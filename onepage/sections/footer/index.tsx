import React from 'react';
import Image from '@siteui/image';
import Title from '@siteui/title';
import Text from '@siteui/text';
import NavLink from '@siteui/navlink';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Footer({ logo, logoAlt, companyLines, phone, phoneHref, email, navTitle, navItems, legalItems, groupLogo, groupAlt, groupHref, groupTitle, copyright }: any) {
  const nav: any[] = Array.isArray(navItems) ? navItems : [];
  const legal: any[] = Array.isArray(legalItems) ? legalItems : [];
  const lines = String(companyLines).split(/\n/).filter((l) => l.trim());
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.top}>
          <div className={styles.brand}>
            {logo && logo.src ? <Image src={logo.src} alt={logoAlt} className={styles.logo} /> : null}
            <div className={styles.lines}>
              {lines.map((l, i) => <Text key={i} size="sm" tone="lightMuted">{l}</Text>)}
            </div>
            <div className={styles.quick}>
              <a href={phoneHref} className={styles.quickLink}><Icon name="phone" size={16} /><span>{phone}</span></a>
              <a href={'mailto:' + email} className={styles.quickLink}><Icon name="mail" size={16} /><span>{email}</span></a>
            </div>
          </div>
          <div className={styles.navCol}>
            <Title as="h3" size="xs" tone="light">{navTitle}</Title>
            <nav className={styles.nav} aria-label={navTitle}>
              {nav.map((it: any, i: number) => <NavLink key={i} href={it.href} tone="light" size="sm">{it.label}</NavLink>)}
            </nav>
          </div>
          <div className={styles.group}>
            <Text size="sm" tone="lightMuted">{groupTitle}</Text>
            <a href={groupHref} target="_blank" rel="noopener noreferrer" aria-label={groupAlt}>
              {groupLogo && groupLogo.src ? <Image src={groupLogo.src} alt={groupAlt} className={styles.groupLogo} /> : null}
            </a>
          </div>
        </div>
        <div className={styles.bottom}>
          <Text size="sm" tone="lightMuted">{copyright}</Text>
          <nav className={styles.legal}>
            {legal.map((it: any, i: number) => <NavLink key={i} href={it.href} tone="light" size="sm">{it.label}</NavLink>)}
          </nav>
        </div>
      </div>
    </footer>
  );
}
