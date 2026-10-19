import React from 'react';
import Image from '@siteui/image';
import styles from './styles.module.css';

function paras(t: any): string[] {
  return String(t || '').split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
}
function rich(p: string) {
  const parts = p.split(/\*\*(.+?)\*\*/g);
  return parts.map((s, i) => (i % 2 === 1 ? <strong key={i}>{s}</strong> : <React.Fragment key={i}>{s}</React.Fragment>));
}

function TextCell({ blocks, logo, logoAlt }: any) {
  const list: any[] = Array.isArray(blocks) ? blocks : [];
  return (
    <div className={styles.textCell}>
      {list.map((b: any, i: number) => (
        <div key={i} className={styles.block}>
          {b.title ? (b.big ? <h2 className={styles.h1}>{b.title}</h2> : <h3 className={styles.h2}>{b.title}</h3>) : null}
          {paras(b.text).map((p, k) => <p key={k} className={styles.p}>{rich(p)}</p>)}
        </div>
      ))}
      {logo && logo.src ? <Image src={logo.src} alt={logoAlt} className={styles.groupLogo} /> : null}
    </div>
  );
}

function Person({ p }: any) {
  return (
    <article className={styles.person}>
      <div className={styles.photo}>{p.photo && p.photo.src ? <Image src={p.photo.src} alt={p.name} className={styles.img} /> : null}</div>
      <div className={styles.info}>
        <h3 className={styles.name}>{p.name}</h3>
        <p className={styles.role}>{p.role}</p>
        <p className={styles.line}>{p.phoneLabel} <a href={p.phoneHref}>{p.phone}</a></p>
        <p className={styles.line}>{p.emailLabel} <a href={'mailto:' + p.email}>{p.email}</a></p>
      </div>
    </article>
  );
}

export default function Team({ introBlocks, valuesBlocks, groupBlocks, groupLogo, groupLogoAlt, people }: any) {
  const ppl: any[] = Array.isArray(people) ? people : [];
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <TextCell blocks={introBlocks} />
        <TextCell blocks={valuesBlocks} />
        <TextCell blocks={groupBlocks} logo={groupLogo} logoAlt={groupLogoAlt} />
        {ppl.map((p: any, i: number) => <Person key={i} p={p} />)}
      </div>
    </section>
  );
}
