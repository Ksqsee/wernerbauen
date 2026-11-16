import React from 'react';
import { mediaUrl } from '@siteui/image';
import styles from './styles.module.css';

export default function PageHero({ image, imageAlt, eyebrow, title, height }: any) {
  const bg = image && image.src ? mediaUrl(image.src, 'xlg2x') : '';
  return (
    <section className={[styles.hero, styles['h_' + height]].join(' ')}>
      <div className={styles.bg} role="img" aria-label={imageAlt} style={{ backgroundImage: bg ? 'url(' + bg + ')' : undefined }} />
      <div className={styles.shade} aria-hidden="true" />
      <div className={styles.inner}>
        {eyebrow ? <p className={styles.eyebrow}>{eyebrow}</p> : null}
        {title ? <h1 className={styles.title}>{title}</h1> : null}
      </div>
    </section>
  );
}
