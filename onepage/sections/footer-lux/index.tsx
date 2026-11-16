import React from 'react';
import Image from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

function Col({ title, items }: any) {
  const list: any[] = Array.isArray(items) ? items : [];
  return (
    <div className={styles.col}>
      <p className={styles.colTitle}>{title}</p>
      <ul className={styles.list}>
        {list.map((it: any, i: number) => <li key={i}><a className={styles.link} href={it.href}>{it.label}</a></li>)}
      </ul>
    </div>
  );
}

export default function Footer({
  logo, logoAlt, claim, ctaLabel, ctaHref,
  contactTitle, company, address, phone, phoneHref, email,
  servicesTitle, serviceItems, companyTitle, companyItems,
  legalItems, copyright, groupTitle, groupLogo, groupAlt, groupHref,
}: any) {
  const legal: any[] = Array.isArray(legalItems) ? legalItems : [];
  const year = new Date().getFullYear();
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.top}>
          <div className={styles.brand}>
            {logo && logo.src ? <Image src={logo.src} alt={logoAlt} className={styles.logo} /> : null}
            {claim ? <p className={styles.claim}>{claim}</p> : null}
          </div>
          {ctaLabel ? <a className={styles.cta} href={ctaHref}>{ctaLabel}<Icon name="arrow" size={16} /></a> : null}
        </div>
        <div className={styles.cols}>
          <div className={styles.col}>
            <p className={styles.colTitle}>{contactTitle}</p>
            <p className={styles.address}>{company}<br />{String(address || '').split('\n').map((l: string, i: number) => <React.Fragment key={i}>{l}<br /></React.Fragment>)}</p>
            <a className={styles.contactLink} href={phoneHref}><Icon name="phone" size={15} />{phone}</a>
            <a className={styles.contactLink} href={'mailto:' + email}><Icon name="mail" size={15} />{email}</a>
          </div>
          <Col title={servicesTitle} items={serviceItems} />
          <Col title={companyTitle} items={companyItems} />
          <div className={styles.col}>
            {groupTitle ? <p className={styles.colTitle}>{groupTitle}</p> : null}
            <a href={groupHref} target="_blank" rel="noopener noreferrer" aria-label={groupAlt} className={styles.group}>
              {groupLogo && groupLogo.src ? <Image src={groupLogo.src} alt={groupAlt} className={styles.groupLogo} /> : null}
            </a>
          </div>
        </div>
        <div className={styles.bottom}>
          <p className={styles.copy}>© {year} {copyright}</p>
          <nav className={styles.legal} aria-label={copyright}>
            {legal.map((it: any, i: number) => <a key={i} className={styles.legalLink} href={it.href}>{it.label}</a>)}
          </nav>
        </div>
      </div>
    </footer>
  );
}
