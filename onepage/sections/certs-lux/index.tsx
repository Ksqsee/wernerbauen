import React from 'react';
import Image from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Certs({ eyebrow, title, items }: any) {
  const list: any[] = Array.isArray(items) ? items : [];
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        {eyebrow || title ? (
          <div className={styles.head}>
            {eyebrow ? <p className={styles.eyebrow}>{eyebrow}</p> : null}
            {title ? <h2 className={styles.heading}>{title}</h2> : null}
          </div>
        ) : null}
        <div className={styles.grid}>
          {list.map((it: any, i: number) => (
            <article key={i} className={styles.item}>
              <div className={styles.logoWrap}>
                {it.logo && it.logo.src ? <Image src={it.logo.src} alt={it.logoAlt} className={styles.logo} /> : null}
              </div>
              <div className={styles.body}>
                <h3 className={styles.title}>{it.title}</h3>
                <p className={styles.text}>{it.text}</p>
                {it.linkLabel && it.linkHref ? <a className={styles.more} href={it.linkHref}>{it.linkLabel}<Icon name="arrow" size={15} /></a> : null}
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
