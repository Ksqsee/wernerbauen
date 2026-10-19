import React from 'react';
import Image from '@siteui/image';
import styles from './styles.module.css';

export default function People({ eyebrow, title, people }: any) {
  const ppl: any[] = Array.isArray(people) ? people : [];
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        {eyebrow || title ? (
          <div className={styles.head}>
            {eyebrow ? <span className={styles.eyebrow}>{eyebrow}</span> : null}
            {title ? <h2 className={styles.title}>{title}</h2> : null}
          </div>
        ) : null}
        <div className={styles.grid}>
          {ppl.map((p: any, i: number) => (
            <article key={i} className={styles.person}>
              <div className={styles.photo}>
                {p.photo && p.photo.src ? <Image src={p.photo.src} alt={p.photoAlt} className={styles.img} /> : null}
              </div>
              <div className={styles.info}>
                <h3 className={styles.name}>{p.name}</h3>
                <p className={styles.role}>{p.role}</p>
                <p className={styles.line}><span className={styles.label}>{p.phoneLabel}</span> <a href={p.phoneHref}>{p.phone}</a></p>
                <p className={styles.line}><span className={styles.label}>{p.emailLabel}</span> <a href={'mailto:' + p.email}>{p.email}</a></p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
