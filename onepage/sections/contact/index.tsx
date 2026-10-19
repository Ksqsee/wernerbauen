import React, { useState } from 'react';
import { crm } from 'onepage-kit';
import Text from '@siteui/text';
import Button from '@siteui/button';
import Icon from '@siteui/icon';
import FormField from '@siteui/form-field';
import styles from './styles.module.css';

const EMPTY = { firstName: '', lastName: '', company: '', phone: '', email: '', message: '' };

export default function Contact({
  infoTitle, companyLines, phoneLabel, phone, phoneHref, faxLabel, fax, emailLabel, email,
  formTitle, firstNameLabel, lastNameLabel, companyLabel, phoneFieldLabel, emailFieldLabel, messageLabel,
  consentPre, consentPost, privacyLabel, privacyHref, requiredNote, submitLabel, sendingLabel, successText, errorText, requiredError, emailError,
  formId,
}: any) {
  const [data, setData] = useState<any>(EMPTY);
  const [errors, setErrors] = useState<any>({});
  const [status, setStatus] = useState<'idle' | 'sending' | 'ok' | 'error'>('idle');
  const lines = String(companyLines).split(/\n/).filter((l) => l.trim());

  const set = (k: string) => (v: string) => setData({ ...data, [k]: v });

  const validate = () => {
    const e: any = {};
    ['firstName', 'lastName', 'email', 'message'].forEach((k) => { if (!String(data[k]).trim()) e[k] = requiredError; });
    if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) e.email = emailError;
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    if (!validate()) return;
    setStatus('sending');
    try {
      await crm.submitForm({ formId, data });
      setStatus('ok');
      setData(EMPTY);
    } catch (err) {
      setStatus('error');
    }
  };

  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <aside className={styles.info}>
          <h1 className={styles.h1}>{infoTitle}</h1>
          <div className={styles.lines}>
            {lines.map((l, i) => <p key={i} className={styles.line}>{l}</p>)}
          </div>
          <div className={styles.lines}>
            <p className={styles.line}>{phoneLabel}: <a href={phoneHref}>{phone}</a></p>
            <p className={styles.line}>{faxLabel}: {fax}</p>
          </div>
          <p className={styles.line}>{emailLabel}: <a className={styles.red} href={'mailto:' + email}>{email}</a></p>
        </aside>

        <div className={styles.formWrap}>
          <h2 className={styles.h1}>{formTitle}</h2>
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
                <FormField id="company" label={companyLabel} value={data.company} onChange={set('company')} autoComplete="organization" />
                <FormField id="phone" label={phoneFieldLabel} type="tel" value={data.phone} onChange={set('phone')} autoComplete="tel" />
              </div>
              <FormField id="email" label={emailFieldLabel} type="email" value={data.email} onChange={set('email')} required error={errors.email} autoComplete="email" />
              <FormField id="message" label={messageLabel} value={data.message} onChange={set('message')} required multiline error={errors.message} />
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
