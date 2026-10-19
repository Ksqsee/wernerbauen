import React from 'react';
import { motion } from 'framer-motion';
import { mediaUrl } from '@siteui/image';
import Title from '@siteui/title';
import Text, { Eyebrow } from '@siteui/text';
import Button from '@siteui/button';
import styles from './styles.module.css';

export default function Hero({ image, imageAlt, eyebrow, title, titleSize, text, primaryLabel, primaryHref, secondaryLabel, secondaryHref, height, overlay, fullHeight }: any) {
  const bg = image && image.src ? mediaUrl(image.src, 'xlg2x') : '';
  const shade = Math.round((Number(overlay) / 100) * 255).toString(16).padStart(2, '0');
  return (
    <section className={[styles.hero, styles['h_' + height], fullHeight ? styles.full : ''].join(' ')}>
      <motion.div
        className={styles.bg}
        role="img"
        aria-label={imageAlt}
        style={{ backgroundImage: bg ? 'url(' + bg + ')' : undefined }}
        initial={{ scale: 1.08 }}
        animate={{ scale: 1 }}
        transition={{ duration: 1.8, ease: [0.22, 1, 0.36, 1] }}
      />
      <div className={styles.shade} style={{ background: 'linear-gradient(180deg, #12121200 25%, #121212' + shade + ' 100%), linear-gradient(90deg, #121212' + shade + ' 0%, #12121200 70%)' }} />
      <div className={styles.container}>
        <motion.div
          className={styles.content}
          initial="hidden"
          animate="show"
          variants={{ hidden: {}, show: { transition: { staggerChildren: 0.12, delayChildren: 0.2 } } }}
        >
          {eyebrow ? (
            <motion.div variants={{ hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0 } }}>
              <Eyebrow tone="light">{eyebrow}</Eyebrow>
            </motion.div>
          ) : null}
          <motion.div variants={{ hidden: { opacity: 0, y: 28 }, show: { opacity: 1, y: 0, transition: { duration: 0.8 } } }}>
            <Title as="h1" size={titleSize} tone="light" uppercase>{title}</Title>
          </motion.div>
          {text ? (
            <motion.div className={styles.text} variants={{ hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } }}>
              <Text size="lg" tone="lightMuted">{text}</Text>
            </motion.div>
          ) : null}
          {primaryLabel || secondaryLabel ? (
            <motion.div className={styles.buttons} variants={{ hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } }}>
              {primaryLabel ? <Button href={primaryHref} variant="primary" size="lg" arrow>{primaryLabel}</Button> : null}
              {secondaryLabel ? <Button href={secondaryHref} variant="outlineLight" size="lg">{secondaryLabel}</Button> : null}
            </motion.div>
          ) : null}
        </motion.div>
      </div>
    </section>
  );
}
