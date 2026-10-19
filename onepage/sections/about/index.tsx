import React from 'react';
import { motion } from 'framer-motion';
import Title from '@siteui/title';
import Text from '@siteui/text';
import Button from '@siteui/button';
import styles from './styles.module.css';

export default function About({ title, subtitle, textLeft, textRight, buttonLabel, buttonHref }: any) {
  return (
    <section className={styles.section}>
      <motion.div
        className={styles.container}
        initial={{ opacity: 0, y: 24 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.25 }}
        transition={{ duration: 0.7 }}
      >
        <div className={styles.head}>
          <Title as="h2" size="md" uppercase>{title}</Title>
          <p className={styles.subtitle}>{subtitle}</p>
        </div>
        <div className={styles.cols}>
          <Text size="md" tone="muted">{textLeft}</Text>
          <div className={styles.right}>
            <Text size="md" tone="muted">{textRight}</Text>
            {buttonLabel ? <div><Button href={buttonHref} variant="link" size="sm" arrow>{buttonLabel}</Button></div> : null}
          </div>
        </div>
      </motion.div>
    </section>
  );
}
