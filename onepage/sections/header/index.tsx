import React, { useState, useEffect, useRef } from 'react';
import Image from '@siteui/image';
import NavLink from '@siteui/navlink';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Header({ logo, logoAlt, logoHref, email, phone, phoneHref, contactLabel, contactHref, applyLabel, applyHref, navItems, activeHref, menuLabel, closeLabel, languages, langLabel }: any) {
  const [open, setOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const langRef = useRef<HTMLDivElement>(null);
  const items: any[] = Array.isArray(navItems) ? navItems : [];
  const langs: any[] = Array.isArray(languages) ? languages : [];
  const current = langs.find((l: any) => l.current) || langs[0];

  useEffect(() => {
    if (!langOpen) return;
    const onDoc = (e: MouseEvent) => { if (langRef.current && !langRef.current.contains(e.target as Node)) setLangOpen(false); };
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setLangOpen(false); };
    document.addEventListener('mousedown', onDoc);
    document.addEventListener('keydown', onKey);
    return () => { document.removeEventListener('mousedown', onDoc); document.removeEventListener('keydown', onKey); };
  }, [langOpen]);
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <a className={styles.logoLink} href={logoHref} aria-label={logoAlt}>
          {logo && logo.src ? <Image src={logo.src} alt={logoAlt} className={styles.logo} /> : null}
        </a>
        <div className={styles.right}>
          <div className={styles.meta}>
            <a className={styles.metaLink} href={'mailto:' + email}>
              <Icon name="mail" size={14} />
              <span>{email}</span>
            </a>
            <span className={styles.sep} aria-hidden="true" />
            <a className={styles.metaLink} href={phoneHref}>
              <Icon name="phone" size={14} />
              <span>{phone}</span>
            </a>
            {applyLabel ? (
              <>
                <span className={styles.sep} aria-hidden="true" />
                <a className={styles.apply} href={applyHref}>
                  <span>{applyLabel}</span>
                  <Icon name="arrow" size={14} />
                </a>
              </>
            ) : null}
            {langs.length > 1 ? (
              <>
                <span className={styles.sep} aria-hidden="true" />
                <div className={styles.lang} ref={langRef}>
                  <button type="button" className={styles.langBtn} aria-haspopup="true" aria-expanded={langOpen} aria-label={langLabel} onClick={() => setLangOpen(!langOpen)}>
                    <Icon name="globe" size={14} />
                    <span>{current ? current.short : null}</span>
                    <span className={[styles.caret, langOpen ? styles.caretOpen : ''].join(' ')}><Icon name="chevron" size={12} /></span>
                  </button>
                  {langOpen ? (
                    <ul className={styles.langList}>
                      {langs.map((l: any, i: number) => (
                        <li key={i}>
                          <a className={[styles.langItem, l.current ? styles.langCurrent : ''].join(' ')} href={l.href} hrefLang={l.code} lang={l.code} aria-current={l.current ? 'true' : undefined}>
                            <span className={styles.langShort}>{l.short}</span>{l.label}
                          </a>
                        </li>
                      ))}
                    </ul>
                  ) : null}
                </div>
              </>
            ) : null}
          </div>
          <div className={styles.navRow}>
            <nav className={styles.nav} aria-label={menuLabel}>
              {items.map((it: any, i: number) => (
                <NavLink key={i} href={it.href} size="sm" active={it.href === activeHref} className={styles.navLink}>{it.label}</NavLink>
              ))}
            </nav>
            <a className={[styles.contact, contactHref === activeHref ? styles.contactActive : ''].join(' ')} href={contactHref}>{contactLabel}</a>
          </div>
        </div>
        <button
          type="button"
          className={styles.burger}
          aria-expanded={open}
          aria-controls="wb-mobile-nav"
          aria-label={open ? closeLabel : menuLabel}
          onClick={() => setOpen(!open)}
        >
          <Icon name={open ? 'close' : 'menu'} size={24} />
        </button>
      </div>
      <div id="wb-mobile-nav" className={[styles.mobile, open ? styles.mobileOpen : ''].join(' ')}>
        <nav className={styles.mobileNav} aria-label={menuLabel}>
          {items.map((it: any, i: number) => (
            <NavLink key={i} href={it.href} active={it.href === activeHref} onClick={() => setOpen(false)} className={styles.mobileLink}>{it.label}</NavLink>
          ))}
          <div className={styles.mobileActions}>
            <a className={styles.contact} href={contactHref} onClick={() => setOpen(false)}>{contactLabel}</a>
            {applyLabel ? <a className={styles.apply} href={applyHref} onClick={() => setOpen(false)}><span>{applyLabel}</span><Icon name="arrow" size={14} /></a> : null}
          </div>
          {langs.length > 1 ? (
            <div className={styles.mobileLangs} aria-label={langLabel}>
              {langs.map((l: any, i: number) => (
                <a key={i} className={[styles.mobileLang, l.current ? styles.langCurrent : ''].join(' ')} href={l.href} hrefLang={l.code} lang={l.code} aria-current={l.current ? 'true' : undefined}>{l.label}</a>
              ))}
            </div>
          ) : null}
        </nav>
      </div>
    </header>
  );
}
