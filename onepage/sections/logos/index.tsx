import React from 'react';
import Image from '@siteui/image';
import styles from './styles.module.css';

export default function Logos({ label, items, seconds }: any) {
  const list: any[] = (Array.isArray(items) ? items : []).filter((x: any) => x && x.logo && x.logo.src);
  if (!list.length) return null;
  const row = (hidden: boolean) => (
    <ul className={styles.row} aria-hidden={hidden ? true : undefined}>
      {[...list, ...list].map((l: any, i: number) => (
        <li key={i} className={styles.item}>
          {l.href ? (
            <a className={styles.link} href={l.href} target="_blank" rel="noopener noreferrer" tabIndex={hidden || i >= list.length ? -1 : undefined}>
              <Image src={l.logo.src} alt={hidden || i >= list.length ? '' : l.alt || l.name} className={styles.logo} />
              <span className={styles.name}>{l.name}</span>
            </a>
          ) : (
            <span className={styles.link}>
              <Image src={l.logo.src} alt={hidden || i >= list.length ? '' : l.alt || l.name} className={styles.logo} />
              <span className={styles.name}>{l.name}</span>
            </span>
          )}
        </li>
      ))}
    </ul>
  );
  return (
    <section className={styles.section} aria-label={label}>
      <div className={styles.inner}>
        {label ? <p className={styles.label}>{label}</p> : null}
        <div className={styles.viewport} style={{ ['--dur' as any]: Math.max(10, Number(seconds) || 36) + 's' }}>
          <div className={styles.track}>
            {row(false)}
            {row(true)}
          </div>
        </div>
      </div>
    </section>
  );
}
