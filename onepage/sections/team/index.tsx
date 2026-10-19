import React from 'react';
import { motion } from 'framer-motion';
import Image from '@siteui/image';
import Title from '@siteui/title';
import Text from '@siteui/text';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Team({ people, tone }: any) {
  const list: any[] = Array.isArray(people) ? people : [];
  return (
    <section className={[styles.section, styles['tone_' + tone]].join(' ')}>
      <div className={styles.container}>
        <div className={styles.grid}>
          {list.map((p: any, i: number) => (
            <motion.article
              key={i}
              className={styles.card}
              initial={{ opacity: 0, y: 32 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.7, delay: i * 0.1 }}
            >
              <div className={styles.photo}>
                {p.photo && p.photo.src ? <Image src={p.photo.src} alt={p.name} className={styles.img} /> : <span className={styles.ph}><Icon name="user" size={56} /></span>}
              </div>
              <div className={styles.info}>
                <Title as="h3" size="sm">{p.name}</Title>
                <Text size="sm" tone="muted">{p.role}</Text>
                <div className={styles.contacts}>
                  <a className={styles.contact} href={p.phoneHref}>
                    <Icon name="phone" size={16} />
                    <span><span className={styles.lbl}>{p.phoneLabel}</span> {p.phone}</span>
                  </a>
                  <a className={styles.contact} href={'mailto:' + p.email}>
                    <Icon name="mail" size={16} />
                    <span><span className={styles.lbl}>{p.emailLabel}</span> {p.email}</span>
                  </a>
                </div>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
