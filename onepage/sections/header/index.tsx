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
              <span className={styles.metaIcon}><Icon name="mail" size={16} /></span>
              <span>{email}</span>
            </a>
            <a className={styles.metaLink} href={phoneHref}>
              <span className={styles.metaIcon}><Icon name="phone" size={16} /></span>
              <span>{phone}</span>
            </a>
            <a className={styles.contact} href={contactHref}>{contactLabel}</a>
            {applyLabel ? <a className={styles.apply} href={applyHref}>{applyLabel}</a> : null}
          </div>
          <nav className={styles.nav} aria-label={menuLabel}>
            {items.map((it: any, i: number) => (
              <NavLink key={i} href={it.href} size="sm" active={it.href === activeHref} className={styles.navLink}>{it.label}</NavLink>
            ))}
          </nav>
        </div>
        <button
          type="button"
          className={styles.burger}
          aria-expanded={open}
          aria-controls="wb-mobile-nav"
          aria-label={open ? closeLabel : menuLabel}
          onClick={() => setOpen(!open)}
        >
          <Icon name={open ? 'close' : 'menu'} size={26} />
        </button>
      </div>
      <div id="wb-mobile-nav" className={[styles.mobile, open ? styles.mobileOpen : ''].join(' ')}>
        <nav className={styles.mobileNav} aria-label={menuLabel}>
          {items.map((it: any, i: number) => (
            <NavLink key={i} href={it.href} active={it.href === activeHref} onClick={() => setOpen(false)} className={styles.mobileLink}>{it.label}</NavLink>
          ))}
          <NavLink href={contactHref} active={contactHref === activeHref} onClick={() => setOpen(false)} className={styles.mobileLink}>{contactLabel}</NavLink>
          {applyLabel ? <a className={[styles.apply, styles.mobileApply].join(' ')} href={applyHref} onClick={() => setOpen(false)}>{applyLabel}</a> : null}
        </nav>
      </div>
    </header>
  );
}
