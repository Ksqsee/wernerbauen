import React from 'react';
import { motion } from 'framer-motion';
import FeatureCard from '@siteui/feature-card';
import styles from './styles.module.css';

export default function Certs({ items, tone }: any) {
  const list: any[] = Array.isArray(items) ? items : [];
  return (
    <section className={[styles.section, styles['tone_' + tone]].join(' ')}>
      <div className={styles.container}>
        <div className={styles.grid}>
          {list.map((it: any, i: number) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 28 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.6, delay: i * 0.08 }}
            >
              <FeatureCard
                logo={it.logo && it.logo.src ? it.logo.src : undefined}
                logoAlt={it.logoAlt}
                title={it.title}
                text={it.text}
                linkLabel={it.linkLabel}
                linkHref={it.linkHref}
                tone={tone === 'dark' ? 'dark' : 'light'}
              />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
