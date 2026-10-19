import React, { useState } from 'react';
import Image from '@siteui/image';
import Button from '@siteui/button';
import NavLink from '@siteui/navlink';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Header({ logo, logoAlt, logoHref, showTopbar, emailLabel, email, phoneLabel, phone, phoneHref, navItems, activeHref, ctaLabel, ctaHref, menuLabel, closeLabel, bgColor }: any) {
  const [open, setOpen] = useState(false);
  const items: any[] = Array.isArray(navItems) ? navItems : [];
  return (
    <header className={styles.header} style={{ background: bgColor }}>
      {showTopbar ? (
        <div className={styles.topbar}>
          <div className={styles.container}>
            <div className={styles.topInner}>
              <a className={styles.topLink} href={'mailto:' + email}>
                <Icon name="mail" size={15} />
                <span>{emailLabel} {email}</span>
              </a>
              <a className={styles.topLink} href={phoneHref}>
                <Icon name="phone" size={15} />
                <span>{phoneLabel} {phone}</span>
              </a>
            </div>
          </div>
        </div>
      ) : null}
      <div className={styles.container}>
        <div className={styles.bar}>
          <a className={styles.logoLink} href={logoHref} aria-label={logoAlt}>
            {logo && logo.src ? <Image src={logo.src} alt={logoAlt} className={styles.logo} /> : null}
          </a>
          <nav className={styles.nav} aria-label={menuLabel}>
            {items.map((it: any, i: number) => (
              <NavLink key={i} href={it.href} active={it.href === activeHref}>{it.label}</NavLink>
            ))}
          </nav>
          <div className={styles.actions}>
            <div className={styles.cta}>
              <Button href={ctaHref} variant="primary" size="sm" arrow>{ctaLabel}</Button>
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
        </div>
      </div>
      <div id="wb-mobile-nav" className={[styles.mobile, open ? styles.mobileOpen : ''].join(' ')}>
        <div className={styles.container}>
          <nav className={styles.mobileNav} aria-label={menuLabel}>
            {items.map((it: any, i: number) => (
              <NavLink key={i} href={it.href} size="lg" active={it.href === activeHref} onClick={() => setOpen(false)}>{it.label}</NavLink>
            ))}
          </nav>
          <div className={styles.mobileCta}>
            <Button href={ctaHref} variant="primary" size="md" arrow>{ctaLabel}</Button>
          </div>
        </div>
      </div>
    </header>
  );
}
