import React, { useState, useEffect, useRef } from 'react';
import Image from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

// Mail provider marks, inline so the header needs no extra dependency.
function brandOf(a: any) {
  const t = (String(a && a.label) + ' ' + String(a && a.url)).toLowerCase();
  if (t.includes('gmail') || t.includes('google')) return 'gmail';
  if (t.includes('outlook') || t.includes('live.com') || t.includes('office')) return 'outlook';
  if (t.includes('gmx')) return 'gmx';
  if (t.includes('web.de')) return 'webde';
  return 'mail';
}
function BrandMark({ name }: { name: string }) {
  const m: Record<string, any> = {
    gmail: (<><path fill="#4285F4" d="M1.5 7.2v10.3c0 .83.67 1.5 1.5 1.5h3.5V10.9z" /><path fill="#34A853" d="M22.5 7.2v10.3c0 .83-.67 1.5-1.5 1.5h-3.5V10.9z" /><path fill="#FBBC04" d="M17.5 6.9l5-3.6v3.9l-5 3.7z" /><path fill="#C5221F" d="M1.5 7.2V6.6c0-1.6 1.8-2.5 3.1-1.6l1.9 1.4v4.5z" /><path fill="#EA4335" d="M6.5 10.9V6.4L12 10.5l5.5-4.1v4.5L12 15z" /></>),
    outlook: (<><rect x="8" y="3" width="15" height="18" rx="2.2" fill="#0A2767" /><path d="M8 5.2C8 4 9 3 10.2 3h10.6C22 3 23 4 23 5.2V10H8z" fill="#0078D4" /><path d="M15.5 3H23v7h-7.5z" fill="#28A8EA" /><path d="M8 10.2l7.5 5.2 7.5-5.2v8.6c0 1.2-1 2.2-2.2 2.2H10.2C9 21 8 20 8 18.8z" fill="#28A8EA" /><rect x="1" y="6.2" width="12.6" height="11.6" rx="2" fill="#0F6CBD" /><ellipse cx="7.3" cy="12" rx="2.9" ry="3.4" fill="none" stroke="#ffffff" strokeWidth="1.9" /></>),
    gmx: (<><rect x="1" y="1" width="22" height="22" rx="5" fill="#1C449B" /><text x="12" y="15" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="8" fontWeight="700" fill="#ffffff">GMX</text></>),
    webde: (<><rect x="1" y="1" width="22" height="22" rx="5" fill="#FFD800" /><text x="12" y="14.2" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="5.6" fontWeight="700" fill="#333333">WEB.DE</text></>),
    mail: (<><rect x="1" y="1" width="22" height="22" rx="5" fill="#D52625" /><rect x="5" y="7.5" width="14" height="9.5" rx="1.5" fill="#ffffff" /><path d="M5.6 8.3L12 13l6.4-4.7" fill="none" stroke="#D52625" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" /></>),
  };
  return <svg width={30} height={30} viewBox="0 0 24 24" aria-hidden="true" focusable="false" className={styles.brand}>{m[name] || m.mail}</svg>;
}

// Keep "@" readable: some desktop mail clients do not decode %40 in mailto links.
function fillTpl(tpl: any, to: string, subject: string) {
  return String(tpl).replace('{to}', encodeURIComponent(to).replace('%40', '@')).replace('{subject}', encodeURIComponent(subject));
}

async function copyText(text: string) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (e) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (err) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }
}

function MailOptions({ address, subject, apps, copyLabel, copiedLabel, copyHint, noAppText, onPick }: any) {
  const [copied, setCopied] = useState(false);
  const [noApp, setNoApp] = useState(false);
  const list: any[] = Array.isArray(apps) ? apps : [];
  const doCopy = async () => {
    if (await copyText(address)) { setCopied(true); window.setTimeout(() => setCopied(false), 2000); }
  };
  // mailto does nothing on computers without a configured mail program: copy first, and say so if the page keeps focus.
  const openMailto = (e: React.MouseEvent, href: string) => {
    e.preventDefault();
    copyText(address);
    setNoApp(false);
    let left = false;
    const onLeave = () => { left = true; };
    window.addEventListener('blur', onLeave);
    document.addEventListener('visibilitychange', onLeave);
    window.location.href = href;
    window.setTimeout(() => {
      window.removeEventListener('blur', onLeave);
      document.removeEventListener('visibilitychange', onLeave);
      if (!left) setNoApp(true);
      else if (onPick) onPick();
    }, 1200);
  };
  return (
    <div className={styles.mailOpts}>
      <button type="button" className={[styles.mailCopy, copied ? styles.mailCopied : ''].join(' ')} onClick={doCopy}>
        <span className={styles.mailAddr}>{address}</span>
        <span className={styles.mailCopyTag}><Icon name={copied ? 'check' : 'copy'} size={15} />{copied ? copiedLabel : copyLabel}</span>
      </button>
      <ul className={styles.mailApps}>
        {list.map((a: any, i: number) => {
          const href = fillTpl(a.url, address, subject);
          const isMailto = href.startsWith('mailto:');
          return (
            <li key={i}>
              <a
                href={href}
                target={isMailto ? undefined : '_blank'}
                rel="noopener noreferrer"
                onClick={(e) => { if (isMailto) { openMailto(e, href); return; } if (a.copy) copyText(address); if (onPick) window.setTimeout(onPick, 250); }}
              >
                <BrandMark name={brandOf(a)} />
                <span className={styles.mailAppName}>{a.label}</span>
                {a.copy ? <small className={styles.mailAppHint}>{copyHint}</small> : null}
                <Icon name="external" size={14} />
              </a>
            </li>
          );
        })}
      </ul>
      {noApp ? <p className={styles.mailNoApp} role="status">{noAppText}</p> : null}
    </div>
  );
}

export default function Header({
  logo, logoAlt, logoHref, navItems, servicesLabel, serviceItems, activeHref, navLang,
  email, emailLabel, mailSubject, mailApps, mailCopyLabel, mailCopiedLabel, mailCopyHint, mailNoApp, phone, phoneHref, contactLabel, contactHref, applyLabel, applyHref,
  whatsappNumber, whatsappText, whatsappLabel, whatsappButton, whatsappFallback,
  languages, langLabel, menuLabel, closeLabel,
}: any) {
  const [open, setOpen] = useState(false);
  const [svcOpen, setSvcOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [mailOpen, setMailOpen] = useState(false);
  const [overlayMail, setOverlayMail] = useState(false);
  const mailRef = useRef<HTMLDivElement>(null);
  const svcRef = useRef<HTMLDivElement>(null);
  const langRef = useRef<HTMLDivElement>(null);
  const items: any[] = Array.isArray(navItems) ? navItems : [];
  const services: any[] = Array.isArray(serviceItems) ? serviceItems : [];
  const langs: any[] = Array.isArray(languages) ? languages : [];
  const current = langs.find((l: any) => l.current) || langs[0];
  const svcActive = services.some((s: any) => s.href === activeHref);
  const waNumber = String(whatsappNumber || '').replace(/[^0-9]/g, '');
  const waHref = waNumber ? 'https://wa.me/' + waNumber + '?text=' + encodeURIComponent(whatsappText) : whatsappFallback;
  const waProps = waNumber ? { target: '_blank', rel: 'noopener noreferrer' } : {};

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    if (!svcOpen && !langOpen && !mailOpen && !open) return;
    const onDoc = (e: MouseEvent | TouchEvent) => {
      if (svcRef.current && !svcRef.current.contains(e.target as Node)) setSvcOpen(false);
      if (langRef.current && !langRef.current.contains(e.target as Node)) setLangOpen(false);
      if (mailRef.current && !mailRef.current.contains(e.target as Node)) setMailOpen(false);
    };
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') { setSvcOpen(false); setLangOpen(false); setMailOpen(false); setOpen(false); } };
    document.addEventListener('mousedown', onDoc);
    document.addEventListener('touchstart', onDoc, { passive: true });
    document.addEventListener('keydown', onKey);
    return () => { document.removeEventListener('mousedown', onDoc); document.removeEventListener('touchstart', onDoc); document.removeEventListener('keydown', onKey); };
  }, [svcOpen, langOpen, mailOpen, open]);

  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, [open]);

  const mailProps = { address: email, subject: mailSubject, apps: mailApps, copyLabel: mailCopyLabel, copiedLabel: mailCopiedLabel, copyHint: mailCopyHint, noAppText: mailNoApp };
  const first = items.slice(0, 1);
  const rest = items.slice(1);
  const link = (it: any, i: number) => (
    <a key={i} href={it.href} className={[styles.link, it.href === activeHref ? styles.linkOn : ''].join(' ')} aria-current={it.href === activeHref ? 'page' : undefined}>{it.label}</a>
  );

  return (
    <header className={[styles.nav, scrolled ? styles.navScrolled : ''].join(' ')}>
      <div className={styles.bar}>
        <a className={styles.logo} href={logoHref} aria-label={logoAlt}>
          {logo && logo.src ? <Image src={logo.src} alt={logoAlt} className={styles.logoImg} /> : null}
        </a>
        <nav className={styles.links} aria-label={menuLabel} lang={navLang}>
          {first.map(link)}
          {services.length ? (
            <div className={styles.svc} ref={svcRef} onMouseEnter={() => setSvcOpen(true)} onMouseLeave={() => setSvcOpen(false)}>
              <button type="button" className={[styles.link, styles.svcBtn, svcActive ? styles.linkOn : ''].join(' ')} aria-expanded={svcOpen} aria-haspopup="true" onClick={() => setSvcOpen(!svcOpen)}>
                {servicesLabel}
                <span className={[styles.caret, svcOpen ? styles.caretOpen : ''].join(' ')}><Icon name="chevron" size={12} /></span>
              </button>
              {svcOpen ? (
                <div className={styles.svcPop}>
                  {services.map((s: any, i: number) => (
                    <a key={i} href={s.href} className={[styles.svcItem, s.href === activeHref ? styles.svcItemOn : ''].join(' ')} aria-current={s.href === activeHref ? 'page' : undefined}>
                      <span>{s.label}</span>
                      <Icon name="arrow" size={14} />
                    </a>
                  ))}
                </div>
              ) : null}
            </div>
          ) : null}
          {rest.map((it: any, i: number) => link(it, i + 1))}
        </nav>
        <div className={styles.actions}>
          {langs.length > 1 ? (
            <div className={styles.lang} ref={langRef}>
              <button type="button" className={styles.langBtn} aria-haspopup="true" aria-expanded={langOpen} aria-label={langLabel} onClick={() => setLangOpen(!langOpen)}>
                <Icon name="globe" size={15} />
                <span>{current ? current.short : null}</span>
              </button>
              {langOpen ? (
                <ul className={styles.langPop}>
                  {langs.map((l: any, i: number) => (
                    <li key={i}>
                      <a className={[styles.langItem, l.current ? styles.langItemOn : ''].join(' ')} href={l.href} hrefLang={l.code} lang={l.code} aria-current={l.current ? 'true' : undefined}>
                        <span className={styles.langShort}>{l.short}</span>{l.label}
                      </a>
                    </li>
                  ))}
                </ul>
              ) : null}
            </div>
          ) : null}
          <a className={styles.wa} href={waHref} {...waProps} aria-label={whatsappLabel}>
            <Icon name="whatsapp" size={20} />
            <span className={styles.pillLabel}>{whatsappButton}</span>
          </a>
          <div className={styles.mailWrap} ref={mailRef}>
            <button type="button" className={[styles.mail, mailOpen ? styles.mailOn : ''].join(' ')} aria-label={emailLabel} aria-expanded={mailOpen} aria-haspopup="true" onClick={() => setMailOpen(!mailOpen)}>
              <span className={styles.mailIcon}><Icon name="mail" size={16} /></span>
              <span className={styles.pillLabel}>{emailLabel}</span>
            </button>
            {mailOpen ? (
              <div className={styles.mailPop}>
                <MailOptions {...mailProps} onPick={() => setMailOpen(false)} />
              </div>
            ) : null}
          </div>
          <a className={styles.phone} href={phoneHref} aria-label={phone}>
            <Icon name="phone" size={16} />
            <span className={styles.pillLabel}>{phone}</span>
          </a>
          <a className={[styles.cta, contactHref === activeHref ? styles.ctaOn : ''].join(' ')} href={contactHref}>{contactLabel}</a>
          <button type="button" className={styles.burger} aria-expanded={open} aria-controls="wb-overlay" aria-label={open ? closeLabel : menuLabel} onClick={() => setOpen(!open)}>
            <Icon name={open ? 'close' : 'menu'} size={22} />
          </button>
        </div>
      </div>

      {open ? (
        <div id="wb-overlay" className={styles.overlay} role="dialog" aria-modal="true" aria-label={menuLabel}>
          <div className={styles.overlayInner}>
            <nav className={styles.overlayNav} lang={navLang} aria-label={menuLabel}>
              {first.map((it: any, i: number) => <a key={'f' + i} href={it.href} className={styles.overlayLink} onClick={() => setOpen(false)}>{it.label}</a>)}
              {services.map((s: any, i: number) => <a key={'s' + i} href={s.href} className={[styles.overlayLink, styles.overlaySub].join(' ')} onClick={() => setOpen(false)}>{s.label}</a>)}
              {rest.map((it: any, i: number) => <a key={'r' + i} href={it.href} className={styles.overlayLink} onClick={() => setOpen(false)}>{it.label}</a>)}
            </nav>
            <div className={styles.overlayActions}>
              <a className={styles.overlayCta} href={contactHref} onClick={() => setOpen(false)}>{contactLabel}</a>
              <a className={styles.overlayWa} href={waHref} {...waProps}><Icon name="whatsapp" size={20} />{whatsappButton}</a>
              <a className={styles.overlayGhost} href={phoneHref}><Icon name="phone" size={16} />{phone}</a>
              <button type="button" className={styles.overlayGhost} aria-expanded={overlayMail} onClick={() => setOverlayMail(!overlayMail)}><Icon name="mail" size={16} />{emailLabel}</button>
              {overlayMail ? <div className={styles.overlayMail}><MailOptions {...mailProps} /></div> : null}
              {applyLabel ? <a className={styles.overlayApply} href={applyHref} onClick={() => setOpen(false)}>{applyLabel}<Icon name="arrow" size={14} /></a> : null}
            </div>
            {langs.length > 1 ? (
              <div className={styles.overlayLangs} aria-label={langLabel}>
                {langs.map((l: any, i: number) => (
                  <a key={i} href={l.href} hrefLang={l.code} lang={l.code} className={[styles.overlayLang, l.current ? styles.overlayLangOn : ''].join(' ')} aria-current={l.current ? 'true' : undefined}>{l.label}</a>
                ))}
              </div>
            ) : null}
          </div>
        </div>
      ) : null}
    </header>
  );
}
