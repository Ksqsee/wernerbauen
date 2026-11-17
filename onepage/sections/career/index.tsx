import React, { useState } from 'react';
import { crm } from 'onepage-kit';
import Text from '@siteui/text';
import Button from '@siteui/button';
import Icon from '@siteui/icon';
import FormField from '@siteui/form-field';
import FileUpload from '@siteui/file-upload';
import styles from './styles.module.css';

const EMPTY = { firstName: '', lastName: '', email: '', phone: '', position: '', message: '' };

function paras(t: any): string[] {
  return String(t || '').split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
}

export default function Career({
  title, intro, benefitsTitle, benefits, initiativeTitle, initiativeText, applyLabel,
  formAnchor, formTitle, formIntro, firstNameLabel, lastNameLabel, emailLabel, phoneLabel, positionLabel, messageLabel,
  attachLabel, attachHint, attachButton, attachRemove, attachTooLarge, attachAccept, attachMaxFiles, attachMaxMb,
  consentPre, privacyLabel, privacyHref, consentPost, requiredNote, submitLabel, sendingLabel, successText, errorText, requiredError, emailError,
  formId, langTitle, langLinks,
}: any) {
  const benefitList: any[] = Array.isArray(benefits) ? benefits : [];
  const langList: any[] = Array.isArray(langLinks) ? langLinks : [];
  const [data, setData] = useState<any>(EMPTY);
  const [files, setFiles] = useState<File[]>([]);
  const [errors, setErrors] = useState<any>({});
  const [status, setStatus] = useState<'idle' | 'sending' | 'ok' | 'error'>('idle');

  const set = (k: string) => (v: string) => setData({ ...data, [k]: v });
  const toForm = () => {
    const el = typeof document !== 'undefined' ? document.getElementById(formAnchor) : null;
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const validate = () => {
    const e: any = {};
    ['firstName', 'lastName', 'email'].forEach((k) => { if (!String(data[k]).trim()) e[k] = requiredError; });
    if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) e.email = emailError;
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    if (!validate()) return;
    setStatus('sending');
    try {
      const attachments = [];
      for (const f of files) attachments.push(await crm.uploadFormFile(f));
      await crm.submitForm({ formId, data: { ...data, attachments } });
      setStatus('ok');
      setData(EMPTY);
      setFiles([]);
    } catch (err) {
      setStatus('error');
    }
  };

  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.top}>
          <div className={styles.intro}>
            {title ? <h1 className={styles.h1}>{title}</h1> : null}
            {langList.filter((l: any) => !l.current).length ? (
              <nav className={styles.langs} aria-label={langTitle}>
                <span className={styles.langsTitle}>{langTitle}</span>
                {langList.filter((l: any) => !l.current).map((l: any, i: number) => (
                  <a key={i} className={styles.langLink} href={l.href} hrefLang={l.code} lang={l.code}>{l.label}</a>
                ))}
              </nav>
            ) : null}
            {paras(intro).map((p, i) => <p key={i} className={i === 0 ? styles.lead : styles.p}>{p}</p>)}
            <div className={styles.cta}>
              <Button href={'#' + formAnchor} variant="primary" size="md" arrow onClick={(e) => { e.preventDefault(); toForm(); }}>{applyLabel}</Button>
            </div>
          </div>
          <div className={styles.benefitsCol}>
            <h2 className={styles.h2}>{benefitsTitle}</h2>
            <ol className={styles.benefits}>
              {benefitList.map((b: any, i: number) => (
                <li key={i} className={styles.benefit}>
                  <span className={styles.num} aria-hidden="true">{String(i + 1).padStart(2, '0')}</span>
                  <span>{b.text}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>

        <div className={styles.initiative}>
          <h2 className={styles.initiativeTitle}>{initiativeTitle}</h2>
          <div className={styles.initiativeBody}>
            {paras(initiativeText).map((p, i) => <p key={i} className={i === 0 ? styles.lead : styles.p}>{p}</p>)}
            <div className={styles.cta}>
              <Button href={'#' + formAnchor} variant="primary" size="md" arrow onClick={(e) => { e.preventDefault(); toForm(); }}>{applyLabel}</Button>
            </div>
          </div>
        </div>

        <div id={formAnchor} className={styles.formWrap}>
          <div className={styles.col}>
            <h2 className={styles.sectionTitle}>{formTitle}</h2>
            {paras(formIntro).map((p, i) => <p key={i} className={styles.p}>{p}</p>)}
          </div>
          {status === 'ok' ? (
            <div className={styles.success} role="status">
              <span className={styles.okIcon}><Icon name="check" size={22} /></span>
              <Text size="md">{successText}</Text>
            </div>
          ) : (
            <form className={styles.form} onSubmit={submit} noValidate>
              <div className={styles.row}>
                <FormField id="firstName" label={firstNameLabel} value={data.firstName} onChange={set('firstName')} required error={errors.firstName} autoComplete="given-name" />
                <FormField id="lastName" label={lastNameLabel} value={data.lastName} onChange={set('lastName')} required error={errors.lastName} autoComplete="family-name" />
              </div>
              <div className={styles.row}>
                <FormField id="email" label={emailLabel} type="email" value={data.email} onChange={set('email')} required error={errors.email} autoComplete="email" />
                <FormField id="phone" label={phoneLabel} type="tel" value={data.phone} onChange={set('phone')} autoComplete="tel" />
              </div>
              <FormField id="position" label={positionLabel} value={data.position} onChange={set('position')} />
              <FormField id="message" label={messageLabel} value={data.message} onChange={set('message')} multiline />
              <FileUpload id="attachments" label={attachLabel} hint={attachHint} buttonLabel={attachButton} removeLabel={attachRemove} tooLargeText={attachTooLarge} accept={attachAccept} maxFiles={Number(attachMaxFiles)} maxSizeMb={Number(attachMaxMb)} files={files} onChange={setFiles} />
              <p className={styles.note}>{consentPre} <a className={styles.red} href={privacyHref}>{privacyLabel}</a> {consentPost}</p>
              <p className={styles.note}>{requiredNote}</p>
              {status === 'error' ? <p className={[styles.note, styles.red].join(' ')}>{errorText}</p> : null}
              <div>
                <Button type="submit" variant="primary" size="md" arrow disabled={status === 'sending'}>
                  {status === 'sending' ? sendingLabel : submitLabel}
                </Button>
              </div>
            </form>
          )}
        </div>
      </div>
    </section>
  );
}
