import React from 'react';
import { motion } from 'framer-motion';
import Image from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Tiles({ eyebrow, title, items, moreLabel }: any) {
  const list: any[] = (Array.isArray(items) ? items : []).filter((x: any) => x && x.title);
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
          {list.map((t: any, i: number) => (
            <motion.a
              key={i}
              href={t.href}
              className={styles.tile}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1], delay: i * 0.12 }}
            >
              <span className={styles.media}>
                {t.image && t.image.src ? <Image src={t.image.src} alt={t.alt || ''} className={styles.img} /> : null}
                <span className={styles.shade} aria-hidden="true" />
              </span>
              <span className={styles.body}>
                <span className={styles.num}>{String(i + 1).padStart(2, '0')}</span>
                <span className={styles.tileTitle}>{t.title}</span>
                {t.text ? <span className={styles.text}>{t.text}</span> : null}
                <span className={styles.more}>{moreLabel}<Icon name="arrow" size={16} /></span>
              </span>
            </motion.a>
          ))}
        </div>
      </div>
    </section>
  );
}
