import React, { useMemo, useState } from 'react';
import { crm } from 'onepage-kit';
import Image from '@siteui/image';
import Icon from '@siteui/icon';
import VoiceNote from './voice';
import styles from './styles.module.css';

function opts(list: any): string[] {
  return (Array.isArray(list) ? list : []).map((o: any) => String(o && o.label ? o.label : '')).filter(Boolean);
}

function Chips({ options, value, multi, onChange }: any) {
  const arr: string[] = Array.isArray(value) ? value : value ? [value] : [];
  return (
    <div className={styles.chips}>
      {options.map((o: string) => {
        const on = arr.includes(o);
        return (
          <button
            key={o}
            type="button"
            className={[styles.chip, on ? styles.chipOn : ''].join(' ')}
            aria-pressed={on}
            onClick={() => onChange(multi ? (on ? arr.filter((x) => x !== o) : [...arr, o]) : o)}
          >
            <span className={styles.box} aria-hidden="true">{on ? <Icon name="check" size={13} /> : null}</span>
            {o}
          </button>
        );
      })}
    </div>
  );
}

function Field({ id, label, required, children, hint }: any) {
  return (
    <div className={styles.field}>
      <label htmlFor={id} className={styles.label}>{label}{required ? <span className={styles.req}> *</span> : null}</label>
      {children}
      {hint ? <span className={styles.hint}>{hint}</span> : null}
    </div>
  );
}

export default function Wizard(props: any) {
  const {
    mode, formId, eyebrow, title, text, checks, timeline, personPhoto, personName, personRole, personLabel, phone, phoneHref, email,
    tabQuickTitle, tabQuickSub, tabFullTitle, tabFullSub,
    qCount, qCountUnit, qCountHint, qUrgency, qServices, qTime, qObject, qPlace, qDescription, qPhotos, qContact, qDamage, qUnits,
    serviceOptions, timeOptions, objectOptions, urgencyOptions, damageOptions,
    lCompany, lName, lPhone, lEmail, lAddress, lAddressPh, lPlace, lPlacePh, lDescription, lDescriptionPh, lUnitLocation, lUnitLocationPh, lTenantName, lTenantContact, lAddUnit, lRemoveUnit, lUnit,
    lPhotos, lPhotosButton, lPhotosHint, lTenantConsent, consentPre, privacyLabel, privacyHref, consentPost,
    voiceLabel, voiceHint, voiceRecord, voiceStop, voiceRecording, voiceDelete, voiceDenied, voiceFileHint,
    nextLabel, backLabel, submitLabel, sendingLabel, successTitle, successText, errorText, requiredError, emailError, contactHint, stepOf,
  } = props;

  const damage = mode === 'damage';
  const [tab, setTab] = useState<'quick' | 'full'>('quick');
  const [step, setStep] = useState(0);
  const [d, setD] = useState<any>({ count: 3, units: [{ location: '', tenant: '', contact: '' }] });
  const [files, setFiles] = useState<File[]>([]);
  const [voice, setVoice] = useState<File | null>(null);
  const [err, setErr] = useState('');
  const [status, setStatus] = useState<'idle' | 'sending' | 'ok' | 'error'>('idle');
  const set = (k: string, v: any) => { setD((x: any) => ({ ...x, [k]: v })); setErr(''); };

  const stepsQuick = damage ? ['count', 'urgency', 'contactQuick'] : ['services', 'time', 'contactQuick'];
  const stepsFull = damage ? ['units', 'damage', 'contactFull'] : ['project', 'place', 'contactFull'];
  const steps = tab === 'quick' ? stepsQuick : stepsFull;
  const cur = steps[step];
  const titles: any = { count: qCount, urgency: qUrgency, services: qServices, time: qTime, contactQuick: qContact, units: qUnits, damage: qDamage, project: qObject, place: qPlace, contactFull: qContact };

  const switchTab = (t: 'quick' | 'full') => { setTab(t); setStep(0); setErr(''); setStatus('idle'); };
  const validEmail = (v: string) => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

  const check = (): string => {
    if (cur === 'contactQuick') {
      if (!String(d.name || '').trim() || !String(d.phone || '').trim()) return requiredError;
      if (!validEmail(d.email || '')) return emailError;
    }
    if (cur === 'contactFull') {
      if (!String(d.name || '').trim() || !String(d.email || '').trim() || (damage && !String(d.phone || '').trim())) return requiredError;
      if (!validEmail(d.email || '')) return emailError;
      if (damage && !d.tenantConsent) return requiredError;
    }
    if (cur === 'units' && !String(d.address || '').trim()) return requiredError;
    if (cur === 'services' && !(d.services || []).length) return requiredError;
    if (cur === 'project' && !(d.services || []).length) return requiredError;
    return '';
  };

  const unitsText = useMemo(() => (d.units || [])
    .filter((u: any) => u.location || u.tenant || u.contact)
    .map((u: any, i: number) => (i + 1) + '. ' + [u.location, u.tenant, u.contact].filter(Boolean).join(' · '))
    .join('\n'), [d.units]);

  const submit = async () => {
    setStatus('sending');
    try {
      const attachments: any[] = [];
      for (const f of files) attachments.push(await crm.uploadFormFile(f));
      if (voice) attachments.push(await crm.uploadFormFile(voice));
      const data: any = {
        requestType: tab === 'quick' ? tabQuickTitle : tabFullTitle,
        company: d.company || '',
        name: d.name || '',
        phone: d.phone || '',
        email: d.email || '',
        description: d.description || '',
        attachments,
      };
      if (damage) {
        Object.assign(data, {
          unitCount: tab === 'quick' ? String(d.count) : String((d.units || []).length),
          urgency: d.urgency || '',
          address: d.address || '',
          units: unitsText,
          damageTypes: (d.damageTypes || []).join(', '),
        });
      } else {
        Object.assign(data, {
          services: (d.services || []).join(', '),
          timeframe: d.time || '',
          objectType: d.objectType || '',
          place: d.place || '',
        });
      }
      await crm.submitForm({ formId, data });
      setStatus('ok');
    } catch (e) {
      setStatus('error');
    }
  };

  const next = () => {
    const m = check();
    if (m) { setErr(m); return; }
    if (step < steps.length - 1) { setStep(step + 1); return; }
    submit();
  };

  const people: any[] = Array.isArray(timeline) ? timeline : [];
  const ticks: any[] = Array.isArray(checks) ? checks : [];
  const addUnit = () => set('units', [...(d.units || []), { location: '', tenant: '', contact: '' }]);
  const setUnit = (i: number, k: string, v: string) => set('units', (d.units || []).map((u: any, j: number) => (j === i ? { ...u, [k]: v } : u)));
  const removeUnit = (i: number) => set('units', (d.units || []).filter((_: any, j: number) => j !== i));

  const photosField = (
    <div className={styles.field}>
      <span className={styles.label}>{lPhotos}</span>
      <label className={styles.drop}>
        <input type="file" multiple accept="image/*,.pdf" className={styles.file} onChange={(e) => { const l = e.target.files; if (l) setFiles((f) => [...f, ...Array.from(l)].slice(0, 8)); e.currentTarget.value = ''; }} />
        <span className={styles.dropIcon}><Icon name="plus" size={18} /></span>
        <span className={styles.dropText}>{lPhotosButton}</span>
        <span className={styles.hint}>{lPhotosHint}</span>
      </label>
      {files.length ? (
        <ul className={styles.files}>
          {files.map((f, i) => (
            <li key={i}><span>{f.name}</span><button type="button" aria-label={lRemoveUnit + ' ' + f.name} onClick={() => setFiles(files.filter((_, j) => j !== i))}><Icon name="close" size={14} /></button></li>
          ))}
        </ul>
      ) : null}
    </div>
  );

  return (
    <section className={styles.section} id={damage ? 'schaden-melden' : 'anfrage'}>
      <div className={styles.container}>
        <div className={styles.left}>
          {eyebrow ? <p className={styles.eyebrow}>{eyebrow}</p> : null}
          <h2 className={styles.title}>{title}</h2>
          {text ? <p className={styles.text}>{text}</p> : null}
          {people.length ? (
            <ol className={styles.timeline}>
              {people.map((t: any, i: number) => (
                <li key={i} className={styles.tl}>
                  <span className={styles.tlBig}>{i === 0 ? <span className={styles.live} aria-hidden="true" /> : null}{t.big}</span>
                  <span className={styles.tlBody}><span className={styles.tlLabel}>{t.label}</span><span className={styles.tlSub}>{t.sub}</span></span>
                </li>
              ))}
            </ol>
          ) : null}
          {ticks.length ? (
            <ul className={styles.ticks}>
              {ticks.map((c: any, i: number) => <li key={i}><span className={styles.tick}><Icon name="check" size={13} /></span>{c.label}</li>)}
            </ul>
          ) : null}
          {personName ? (
            <div className={styles.person}>
              {personPhoto && personPhoto.src ? <Image src={personPhoto.src} alt={personName} className={styles.personImg} /> : null}
              <div>
                <p className={styles.personLabel}>{personLabel}</p>
                <p className={styles.personName}>{personName}</p>
                <p className={styles.personRole}>{personRole}</p>
              </div>
            </div>
          ) : null}
          <div className={styles.direct}>
            <a className={styles.directPrimary} href={phoneHref}><span className={[styles.tile, styles.tilePhone].join(' ')}><Icon name="phone" size={15} /></span>{phone}</a>
            <a className={styles.directGhost} href={'mailto:' + email}><span className={[styles.tile, styles.tileMail].join(' ')}><Icon name="mail" size={15} /></span>{email}</a>
          </div>
        </div>

        <div className={styles.panel}>
          <div className={styles.tabs} role="tablist">
            <button type="button" role="tab" aria-selected={tab === 'quick'} className={[styles.tab, tab === 'quick' ? styles.tabOn : ''].join(' ')} onClick={() => switchTab('quick')}>
              <span className={styles.tabTitle}>{tabQuickTitle}</span><span className={styles.tabSub}>{tabQuickSub}</span>
            </button>
            <button type="button" role="tab" aria-selected={tab === 'full'} className={[styles.tab, tab === 'full' ? styles.tabOn : ''].join(' ')} onClick={() => switchTab('full')}>
              <span className={styles.tabTitle}>{tabFullTitle}</span><span className={styles.tabSub}>{tabFullSub}</span>
            </button>
          </div>

          {status === 'ok' ? (
            <div className={styles.done} role="status">
              <span className={styles.doneIcon}><Icon name="check" size={24} /></span>
              <p className={styles.doneTitle}>{successTitle}</p>
              <p className={styles.doneText}>{successText}</p>
            </div>
          ) : (
            <form className={styles.form} onSubmit={(e) => { e.preventDefault(); next(); }} noValidate>
              <div className={styles.stepHead}>
                <span className={styles.stepNum}>{step + 1}{stepOf}{steps.length}</span>
                <h3 className={styles.stepTitle}>{titles[cur]}</h3>
              </div>
              <div className={styles.bar}><span style={{ width: ((step + 1) / steps.length) * 100 + '%' }} /></div>

              {cur === 'count' ? (
                <div className={styles.range}>
                  <p className={styles.rangeValue}><span>{d.count >= 20 ? '20+' : d.count}</span> {qCountUnit}</p>
                  <input type="range" min={1} max={20} value={d.count} onChange={(e) => set('count', Number(e.target.value))} aria-label={qCount} />
                  <div className={styles.rangeScale}><span>1</span><span>{qCountHint}</span><span>20+</span></div>
                </div>
              ) : null}
              {cur === 'urgency' ? <Chips options={opts(urgencyOptions)} value={d.urgency} onChange={(v: any) => set('urgency', v)} /> : null}
              {cur === 'services' ? <Chips options={opts(serviceOptions)} value={d.services} multi onChange={(v: any) => set('services', v)} /> : null}
              {cur === 'time' ? <Chips options={opts(timeOptions)} value={d.time} onChange={(v: any) => set('time', v)} /> : null}

              {cur === 'project' ? (
                <>
                  <Chips options={opts(serviceOptions)} value={d.services} multi onChange={(v: any) => set('services', v)} />
                  <div className={styles.sub}>{qTime}</div>
                  <Chips options={opts(timeOptions)} value={d.time} onChange={(v: any) => set('time', v)} />
                </>
              ) : null}
              {cur === 'place' ? (
                <>
                  <Chips options={opts(objectOptions)} value={d.objectType} onChange={(v: any) => set('objectType', v)} />
                  <Field id="wz-place" label={lPlace}><input id="wz-place" className={styles.input} value={d.place || ''} placeholder={lPlacePh} onChange={(e) => set('place', e.target.value)} /></Field>
                  <Field id="wz-desc" label={lDescription}><textarea id="wz-desc" className={styles.input} rows={4} value={d.description || ''} placeholder={lDescriptionPh} onChange={(e) => set('description', e.target.value)} /></Field>
                  <VoiceNote dark value={voice} onChange={setVoice} label={voiceLabel} hint={voiceHint} recordLabel={voiceRecord} stopLabel={voiceStop} recordingLabel={voiceRecording} deleteLabel={voiceDelete} deniedText={voiceDenied} fileHint={voiceFileHint} filePrefix={damage ? 'schaden-sprachnachricht' : 'projekt-sprachnachricht'} />
                  {photosField}
                </>
              ) : null}

              {cur === 'units' ? (
                <>
                  <Field id="wz-address" label={lAddress} required><input id="wz-address" className={styles.input} value={d.address || ''} placeholder={lAddressPh} onChange={(e) => set('address', e.target.value)} /></Field>
                  {(d.units || []).map((u: any, i: number) => (
                    <div key={i} className={styles.unit}>
                      <div className={styles.unitHead}>
                        <span>{lUnit} {i + 1}</span>
                        {i > 0 ? <button type="button" className={styles.unitRemove} onClick={() => removeUnit(i)}>{lRemoveUnit}</button> : null}
                      </div>
                      <div className={styles.row}>
                        <Field id={'wz-loc' + i} label={lUnitLocation}><input id={'wz-loc' + i} className={styles.input} value={u.location} placeholder={lUnitLocationPh} onChange={(e) => setUnit(i, 'location', e.target.value)} /></Field>
                        <Field id={'wz-ten' + i} label={lTenantName}><input id={'wz-ten' + i} className={styles.input} value={u.tenant} onChange={(e) => setUnit(i, 'tenant', e.target.value)} /></Field>
                      </div>
                      <Field id={'wz-con' + i} label={lTenantContact}><input id={'wz-con' + i} className={styles.input} value={u.contact} onChange={(e) => setUnit(i, 'contact', e.target.value)} /></Field>
                    </div>
                  ))}
                  <button type="button" className={styles.add} onClick={addUnit}><Icon name="plus" size={15} />{lAddUnit}</button>
                </>
              ) : null}
              {cur === 'damage' ? (
                <>
                  <Chips options={opts(damageOptions)} value={d.damageTypes} multi onChange={(v: any) => set('damageTypes', v)} />
                  <div className={styles.sub}>{qUrgency}</div>
                  <Chips options={opts(urgencyOptions)} value={d.urgency} onChange={(v: any) => set('urgency', v)} />
                  <Field id="wz-desc2" label={lDescription}><textarea id="wz-desc2" className={styles.input} rows={4} value={d.description || ''} placeholder={lDescriptionPh} onChange={(e) => set('description', e.target.value)} /></Field>
                  <VoiceNote dark value={voice} onChange={setVoice} label={voiceLabel} hint={voiceHint} recordLabel={voiceRecord} stopLabel={voiceStop} recordingLabel={voiceRecording} deleteLabel={voiceDelete} deniedText={voiceDenied} fileHint={voiceFileHint} filePrefix={damage ? 'schaden-sprachnachricht' : 'projekt-sprachnachricht'} />
                  {photosField}
                </>
              ) : null}

              {cur === 'contactQuick' || cur === 'contactFull' ? (
                <>
                  <Field id="wz-company" label={lCompany}><input id="wz-company" className={styles.input} value={d.company || ''} onChange={(e) => set('company', e.target.value)} autoComplete="organization" /></Field>
                  <Field id="wz-name" label={lName} required><input id="wz-name" className={styles.input} value={d.name || ''} onChange={(e) => set('name', e.target.value)} autoComplete="name" /></Field>
                  <div className={styles.row}>
                    <Field id="wz-phone" label={lPhone} required={cur === 'contactQuick' || damage}><input id="wz-phone" type="tel" className={styles.input} value={d.phone || ''} onChange={(e) => set('phone', e.target.value)} autoComplete="tel" /></Field>
                    <Field id="wz-email" label={lEmail} required={cur === 'contactFull'}><input id="wz-email" type="email" className={styles.input} value={d.email || ''} onChange={(e) => set('email', e.target.value)} autoComplete="email" /></Field>
                  </div>
                  {cur === 'contactQuick' ? <p className={styles.hint}>{contactHint}</p> : null}
                  {cur === 'contactQuick' ? <VoiceNote dark value={voice} onChange={setVoice} label={voiceLabel} hint={voiceHint} recordLabel={voiceRecord} stopLabel={voiceStop} recordingLabel={voiceRecording} deleteLabel={voiceDelete} deniedText={voiceDenied} fileHint={voiceFileHint} filePrefix={damage ? 'schaden-sprachnachricht' : 'projekt-sprachnachricht'} /> : null}
                  {cur === 'contactFull' && damage ? (
                    <label className={styles.consent}>
                      <input type="checkbox" checked={!!d.tenantConsent} onChange={(e) => set('tenantConsent', e.target.checked)} />
                      <span className={styles.box} aria-hidden="true">{d.tenantConsent ? <Icon name="check" size={13} /> : null}</span>
                      <span>{lTenantConsent}</span>
                    </label>
                  ) : null}
                  <p className={styles.legal}>{consentPre} <a href={privacyHref}>{privacyLabel}</a> {consentPost}</p>
                </>
              ) : null}

              {err ? <p className={styles.error} role="alert">{err}</p> : null}
              {status === 'error' ? <p className={styles.error} role="alert">{errorText}</p> : null}

              <div className={styles.nav}>
                {step > 0 ? <button type="button" className={styles.back} onClick={() => { setStep(step - 1); setErr(''); }}>{backLabel}</button> : <span />}
                <button type="submit" className={styles.next} disabled={status === 'sending'}>
                  {status === 'sending' ? sendingLabel : step === steps.length - 1 ? submitLabel : nextLabel}
                  <Icon name="arrow" size={16} />
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </section>
  );
}
