import React from 'react';
import Image, { mediaUrl } from '@siteui/image';
import Text from '@siteui/text';
import NavLink from '@siteui/navlink';
import styles from './styles.module.css';

export default function Footer({ background, logo, logoAlt, groupTitle, groupLogo, groupAlt, groupHref, legalItems }: any) {
  const legal: any[] = Array.isArray(legalItems) ? legalItems : [];
  const bg = background && background.src ? mediaUrl(background.src, 'xlg') : '';
  return (
    <footer className={styles.footer} style={{ backgroundImage: bg ? 'linear-gradient(180deg, #12121233, #121212b3), url(' + bg + ')' : undefined }}>
      <div className={styles.container}>
        <div className={styles.brand}>
          {logo && logo.src ? <Image src={logo.src} alt={logoAlt} className={styles.logo} /> : null}
          {groupTitle ? <Text as="span" size="sm" tone="lightMuted" className={styles.groupTitle}>{groupTitle}</Text> : null}
          <a href={groupHref} target="_blank" rel="noopener noreferrer" aria-label={groupAlt}>
            {groupLogo && groupLogo.src ? <Image src={groupLogo.src} alt={groupAlt} className={styles.groupLogo} /> : null}
          </a>
        </div>
        <nav className={styles.legal}>
          {legal.map((it: any, i: number) => <NavLink key={i} href={it.href} tone="light" size="sm">{it.label}</NavLink>)}
        </nav>
      </div>
    </footer>
  );
}
