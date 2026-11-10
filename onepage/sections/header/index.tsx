import React, { useState, useEffect, useRef } from 'react';
import Image from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Header({
  logo, logoAlt, logoHref, navItems, servicesLabel, serviceItems, activeHref, navLang,
  email, emailLabel, phone, phoneHref, contactLabel, contactHref, applyLabel, applyHref,
  whatsappNumber, whatsappText, whatsappLabel, whatsappButton, whatsappFallback,
  languages, langLabel, menuLabel, closeLabel,
}: any) {
  const [open, setOpen] = useState(false);
  const [svcOpen, setSvcOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
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
    if (!svcOpen && !langOpen && !open) return;
    const onDoc = (e: MouseEvent) => {
      if (svcRef.current && !svcRef.current.contains(e.target as Node)) setSvcOpen(false);
      if (langRef.current && !langRef.current.contains(e.target as Node)) setLangOpen(false);
    };
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') { setSvcOpen(false); setLangOpen(false); setOpen(false); } };
    document.addEventListener('mousedown', onDoc);
    document.addEventListener('keydown', onKey);
    return () => { document.removeEventListener('mousedown', onDoc); document.removeEventListener('keydown', onKey); };
  }, [svcOpen, langOpen, open]);

  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, [open]);

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
          <a className={styles.mail} href={'mailto:' + email} aria-label={emailLabel + ': ' + email}>
            <span className={styles.mailIcon}><Icon name="mail" size={16} /></span>
            <span className={styles.pillLabel}>{emailLabel}</span>
          </a>
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
              <a className={styles.overlayGhost} href={'mailto:' + email}><Icon name="mail" size={16} />{email}</a>
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
