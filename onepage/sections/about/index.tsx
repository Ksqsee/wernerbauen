import React from 'react';
import Title from '@siteui/title';
import Text from '@siteui/text';
import Button from '@siteui/button';
import styles from './styles.module.css';

export default function About({ title, subtitle, textLeft, textRight, buttonLabel, buttonHref }: any) {
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.head}>
          <Title as="h2" size="lg" uppercase>{title}</Title>
          <p className={styles.subtitle}>{subtitle}</p>
        </div>
        <div className={styles.body}>
          <Text size="md" tone="muted">{textLeft}</Text>
          <Text size="md" tone="muted">{textRight}</Text>
          {buttonLabel ? <div className={styles.more}><Button href={buttonHref} variant="link" size="md" arrow>{buttonLabel}</Button></div> : null}
        </div>
      </div>
    </section>
  );
}
