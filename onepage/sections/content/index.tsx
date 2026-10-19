import React from 'react';
import { motion } from 'framer-motion';
import Image from '@siteui/image';
import Title from '@siteui/title';
import Text, { Eyebrow } from '@siteui/text';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

function splitParas(t: any): string[] {
  return String(t || '').split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
}
function splitLines(t: any): string[] {
  return String(t || '').split(/\n/).map((p) => p.trim()).filter(Boolean);
}

export default function Content({ blocks, tone, compact }: any) {
  const list: any[] = Array.isArray(blocks) ? blocks : [];
  const dark = tone === 'dark';
  return (
    <section className={[styles.section, styles['tone_' + tone], compact ? styles.compact : ''].join(' ')}>
      <div className={styles.container}>
        {list.map((b: any, i: number) => {
          const hasImage = b.layout !== 'text' && b.image && b.image.src;
          const paras = splitParas(b.text);
          const bullets = splitLines(b.bullets);
          const after = splitParas(b.textAfter);
          const body = (
            <div className={styles.body}>
              {paras.map((p, k) => (
                <Text key={k} size={b.lead && k === 0 ? 'lg' : 'md'} tone={dark ? 'lightMuted' : 'dark'} className={b.lead && k === 0 ? styles.lead : ''}>{p}</Text>
              ))}
              {bullets.length ? (
                <ul className={styles.list}>
                  {bullets.map((li, k) => (
                    <li key={k} className={styles.item}>
                      <span className={styles.check}><Icon name="check" size={16} /></span>
                      <Text as="span" size="md" tone={dark ? 'light' : 'dark'}>{li}</Text>
                    </li>
                  ))}
                </ul>
              ) : null}
              {after.map((p, k) => <Text key={'a' + k} size="md" tone={dark ? 'lightMuted' : 'dark'}>{p}</Text>)}
            </div>
          );
          const head = (
            <div className={styles.head}>
              {b.eyebrow ? <Eyebrow tone={dark ? 'light' : 'dark'}>{b.eyebrow}</Eyebrow> : null}
              {b.title ? <Title as={b.h1 ? 'h1' : 'h2'} size={b.h1 ? 'xl' : 'lg'} tone={dark ? 'light' : 'dark'}>{b.title}</Title> : null}
            </div>
          );
          return (
            <motion.article
              key={i}
              className={[styles.block, hasImage ? styles.split : styles.textOnly, hasImage && b.layout === 'imageLeft' ? styles.imgLeft : ''].join(' ')}
              initial={{ opacity: 0, y: 36 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.15 }}
              transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
            >
              {hasImage ? (
                <>
                  <div className={styles.col}>
                    {head}
                    {body}
                  </div>
                  <div className={styles.media}>
                    <Image src={b.image.src} alt={b.imageAlt} className={styles.img} />
                  </div>
                </>
              ) : (
                <>
                  {head}
                  {body}
                </>
              )}
            </motion.article>
          );
        })}
      </div>
    </section>
  );
}
