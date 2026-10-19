import React from 'react';
import Image from '@siteui/image';
import Button from '@siteui/button';
import styles from './styles.module.css';

export default function Certs({ items }: any) {
  const list: any[] = Array.isArray(items) ? items : [];
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        {list.map((it: any, i: number) => (
          <article key={i} className={styles.item}>
            <div className={styles.logoWrap}>
              {it.logo && it.logo.src ? <Image src={it.logo.src} alt={it.logoAlt} className={styles.logo} /> : null}
            </div>
            <div className={styles.body}>
              <h3 className={styles.title}>{it.title}</h3>
              <p className={styles.text}>{it.text}</p>
              {it.linkLabel && it.linkHref ? <div><Button href={it.linkHref} variant="link" size="sm" arrow>{it.linkLabel}</Button></div> : null}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
