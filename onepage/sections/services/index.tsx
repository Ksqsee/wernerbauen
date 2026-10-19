import React from 'react';
import { motion } from 'framer-motion';
import Image, { mediaUrl } from '@siteui/image';
import Text from '@siteui/text';
import Button from '@siteui/button';
import styles from './styles.module.css';

export default function Services({ bannerImage, bannerAlt, anchorId, items }: any) {
  const list: any[] = Array.isArray(items) ? items : [];
  const bg = bannerImage && bannerImage.src ? mediaUrl(bannerImage.src, 'xlg2x') : '';
  return (
    <section id={anchorId} className={styles.section}>
      <div className={styles.banner} role="img" aria-label={bannerAlt} style={{ backgroundImage: bg ? 'url(' + bg + ')' : undefined }} />
      <div className={styles.container}>
        <div className={styles.grid}>
          {list.map((it: any, i: number) => (
            <motion.article
              key={i}
              className={styles.col}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.7, delay: i * 0.1, ease: [0.22, 1, 0.36, 1] }}
            >
              <a className={styles.card} href={it.linkHref}>
                <h2 className={styles.label}>{it.title}</h2>
                <div className={styles.media}>
                  {it.image && it.image.src ? <Image src={it.image.src} alt={it.imageAlt} className={styles.img} /> : null}
                  <span className={styles.pointer} aria-hidden="true" />
                </div>
              </a>
              <div className={styles.body}>
                <Text size="sm" tone="muted">{it.text}</Text>
                {it.linkLabel ? (
                  <div className={styles.more}>
                    <Button href={it.linkHref} variant="link" size="sm" arrow>{it.linkLabel}</Button>
                  </div>
                ) : null}
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
