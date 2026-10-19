import React, { useState } from 'react';
import Image from '@siteui/image';
import NavLink from '@siteui/navlink';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Header({ logo, logoAlt, logoHref, email, phone, phoneHref, contactLabel, contactHref, applyLabel, applyHref, navItems, activeHref, menuLabel, closeLabel }: any) {
  const [open, setOpen] = useState(false);
  const items: any[] = Array.isArray(navItems) ? navItems : [];
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
        </nav>
      </div>
    </header>
  );
}
