import React from 'react';
import { motion } from 'framer-motion';
import Image from '@siteui/image';
import Title from '@siteui/title';
import Text, { Eyebrow } from '@siteui/text';
import Button from '@siteui/button';
import styles from './styles.module.css';

export default function About({ image, imageAlt, eyebrow, title, text, buttonLabel, buttonHref, bgColor }: any) {
  const paragraphs = String(text).split(/\n\s*\n/).filter((p) => p.trim());
  return (
    <section className={styles.section} style={{ background: bgColor }}>
      <div className={styles.container}>
        <motion.div
          className={styles.media}
          initial={{ opacity: 0, scale: 0.96 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
        >
          {image && image.src ? <Image src={image.src} alt={imageAlt} className={styles.img} /> : null}
        </motion.div>
        <motion.div
          className={styles.body}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.8, delay: 0.15 }}
        >
          <Eyebrow tone="light">{eyebrow}</Eyebrow>
          <Title as="h2" size="xl" tone="light">{title}</Title>
          <div className={styles.paras}>
            {paragraphs.map((p, i) => <Text key={i} size="md" tone="lightMuted">{p}</Text>)}
          </div>
          {buttonLabel ? (
            <div className={styles.btn}>
              <Button href={buttonHref} variant="primary" size="lg" arrow>{buttonLabel}</Button>
            </div>
          ) : null}
        </motion.div>
      </div>
    </section>
  );
}
