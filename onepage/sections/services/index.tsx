import React from 'react';
import { motion } from 'framer-motion';
import Image from '@siteui/image';
import Title from '@siteui/title';
import Text from '@siteui/text';
import Button from '@siteui/button';
import styles from './styles.module.css';

export default function Services({ anchorId, items, bgColor }: any) {
  const list: any[] = Array.isArray(items) ? items : [];
  return (
    <section id={anchorId} className={styles.section} style={{ background: bgColor }}>
      <div className={styles.container}>
        {list.map((it: any, i: number) => (
          <motion.article
            key={i}
            className={[styles.row, i % 2 === 1 ? styles.reverse : ''].join(' ')}
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.25 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          >
            <a className={styles.media} href={it.buttonHref} tabIndex={-1} aria-hidden="true">
              {it.image && it.image.src ? <Image src={it.image.src} alt={it.imageAlt} className={styles.img} /> : null}
              <span className={styles.num}>{String(i + 1).padStart(2, '0')}</span>
            </a>
            <div className={styles.body}>
              <Title as="h2" size="lg" uppercase>{it.title}</Title>
              <Text size="md" tone="muted">{it.text}</Text>
              {it.buttonLabel ? (
                <div className={styles.btn}>
                  <Button href={it.buttonHref} variant="dark" size="md" arrow>{it.buttonLabel}</Button>
                </div>
              ) : null}
            </div>
          </motion.article>
        ))}
      </div>
    </section>
  );
}
