import { useState, useEffect } from "react";

const API = "http://127.0.0.1:5000";

function getSanatoriumImage(id) {
  return `/images/sanat_${id}.png`;
}

export default function App() {
  const [user, setUser] = useState(null);
  const [page, setPage] = useState("recommend");
  const [tags, setTags] = useState([]);
  const [results, setResults] = useState([]);
  const [catalog, setCatalog] = useState([]);
  const [compareIds, setCompareIds] = useState([]);
  const [selectedSanatorium, setSelectedSanatorium] = useState(null);
  const [selectedTags, setSelectedTags] = useState([]);
  const [budget, setBudget] = useState(5000);
  const [region, setRegion] = useState("");
  const [goal, setGoal] = useState("отдых");
  const [budgetWeight, setBudgetWeight] = useState(5);
  const [regionWeight, setRegionWeight] = useState(3);
  const [medicalWeight, setMedicalWeight] = useState(5);
  const [servicesWeight, setServicesWeight] = useState(3);
  const [conditionsWeight, setConditionsWeight] = useState(3);

  // Состояние отзывов
  const [reviews, setReviews] = useState([]);
  const [reviewText, setReviewText] = useState("");
  const [reviewRating, setReviewRating] = useState(5);

  // Смена пароля
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [passwordMsg, setPasswordMsg] = useState("");

  useEffect(() => {
    if (user) {
      fetch(`${API}/api/tags`).then(r => r.json()).then(setTags);
      fetch(`${API}/api/sanatoriums/`).then(r => r.json()).then(setCatalog);
      fetch(`${API}/api/recommend`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: user.id })
      }).then(r => r.ok ? r.json() : []).then(d => Array.isArray(d) && setResults(d)).catch(() => setResults([]));
    }
  }, [user]);

  // Загрузка отзывов при открытии детальной страницы
  useEffect(() => {
    if (page === "detail" && selectedSanatorium) {
      fetch(`${API}/api/reviews/${selectedSanatorium.id}`)
        .then(r => r.json())
        .then(d => Array.isArray(d) ? setReviews(d) : setReviews([]))
        .catch(() => setReviews([]));
    }
  }, [page, selectedSanatorium]);

  function toggleTag(tagId) {
    setSelectedTags(prev => prev.includes(tagId) ? prev.filter(id => id !== tagId) : [...prev, tagId]);
  }

  function saveProfile() {
    fetch(`${API}/api/profile`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: user.id, goal, budget, region, tag_ids: selectedTags, budget_weight: budgetWeight, region_weight: regionWeight, medical_weight: medicalWeight, services_weight: servicesWeight, conditions_weight: conditionsWeight })
    }).then(r => r.json()).then(() => {
      fetch(`${API}/api/recommend`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: user.id })
      }).then(r => r.json()).then(d => { setResults(d); setPage("recommend"); });
    });
  }

  function toggleCompare(id) {
    setCompareIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : prev.length < 3 ? [...prev, id] : prev);
  }

  function getRegions() { return [...new Set(catalog.map(s => s.region))].sort(); }

  function openDetail(sanatorium, from) {
    setSelectedSanatorium({ ...sanatorium, _from: from });
    setPage("detail");
    setReviewText("");
    setReviewRating(5);
  }

  // Отправить отзыв
  function submitReview() {
    if (!reviewText.trim()) return;
    fetch(`${API}/api/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: user.id,
        sanatorium_id: selectedSanatorium.id,
        text: reviewText,
        rating: reviewRating
      })
    })
      .then(r => r.json())
      .then(() => {
        // Перезагрузить отзывы
        fetch(`${API}/api/reviews/${selectedSanatorium.id}`)
          .then(r => r.json())
          .then(d => setReviews(d));
        setReviewText("");
        setReviewRating(5);
      });
  }

  if (!user) return <AuthScreen onLogin={setUser} />;

  return (
    <div style={S.app}>
      <header style={S.header}><div style={S.headerInner}>
        <h1 style={S.logo}>🏥 Подбор Санатория</h1>
        <nav style={S.nav}>
          <NavBtn a={page === "recommend"} o={() => setPage("recommend")}>📋 Рекомендации</NavBtn>
          <NavBtn a={page === "profile"} o={() => setPage("profile")}>⚙️ Профиль</NavBtn>
          <NavBtn a={page === "catalog"} o={() => setPage("catalog")}>🏨 Каталог</NavBtn>
          {compareIds.length > 0 && <NavBtn a={page === "compare"} o={() => setPage("compare")}>⚖️ Сравнение ({compareIds.length})</NavBtn>}
        </nav>
        <div style={S.userBlock}>
          <span onClick={() => { setPage("settings"); setPasswordMsg(""); setOldPassword(""); setNewPassword(""); }} style={{ ...S.userName, cursor: "pointer", textDecoration: "underline" }}>{user.name}</span>
          <button onClick={() => { setUser(null); setResults([]); }} style={S.logoutBtn}>Выйти</button>
        </div>
      </div></header>

      <main style={S.main}>

        {/* ======== ДЕТАЛЬНЫЙ ПРОСМОТР ======== */}
        {page === "detail" && selectedSanatorium && (
          <div>
            <button onClick={() => setPage(selectedSanatorium._from || "recommend")} style={S.backBtn}>← Назад</button>

            {/* Картинка санатория */}
            <div style={S.detailImageWrap}>
              <img src={getSanatoriumImage(selectedSanatorium.id)} alt={selectedSanatorium.name} style={S.detailImage} />
              <div style={S.detailImageOverlay}>
                <h2 style={S.detailImageName}>{selectedSanatorium.name}</h2>
                <p style={S.detailImageRegion}>📍 {selectedSanatorium.region}</p>
              </div>
            </div>

            <div style={S.detailCard}>
              {selectedSanatorium.score !== undefined && (
                <div style={S.detailScoreBar}>
                  <span>Оценка соответствия (Weighted Goal Programming):</span>
                  <span style={S.detailScoreVal}>Score: {selectedSanatorium.score}</span>
                </div>
              )}

              <div style={S.detailGrid}>
                <DetailInfo icon="💰" label="Цена за сутки" value={`${selectedSanatorium.budget.toLocaleString()} ₽`} />
                <DetailInfo icon="🍽️" label="Питание" value={selectedSanatorium.food} />
                <DetailInfo icon="📍" label="Регион" value={selectedSanatorium.region} />
                <DetailInfo icon="⭐" label="Рейтинг" value={`${selectedSanatorium.rating} / 5.0`} />
              </div>

              <DetailTagSection title="🏥 Медицинский профиль" tags={selectedSanatorium.tags} cat="medical" bg="#eff6ff" fg="#1d4ed8" />
              <DetailTagSection title="🛎️ Услуги" tags={selectedSanatorium.tags} cat="services" bg="#f0fdf4" fg="#15803d" />
              <DetailTagSection title="🏠 Условия проживания" tags={selectedSanatorium.tags} cat="conditions" bg="#fff7ed" fg="#c2410c" />

              <div style={{ marginTop: 24, display: "flex", gap: 12 }}>
                <button onClick={() => toggleCompare(selectedSanatorium.id)}
                  style={compareIds.includes(selectedSanatorium.id) ? S.compareActiveBtn : S.compareBtn}>
                  {compareIds.includes(selectedSanatorium.id) ? "✓ В сравнении" : "⚖️ Добавить к сравнению"}
                </button>
              </div>

              {/* ======== БЛОК ОТЗЫВОВ ======== */}
              <div style={S.reviewsSection}>
                <h3 style={S.reviewsTitle}>💬 Отзывы ({reviews.length})</h3>

                {/* Форма нового отзыва */}
                <div style={S.reviewForm}>
                  <div style={S.reviewFormHeader}>
                    <span style={S.reviewFormLabel}>Ваша оценка:</span>
                    <div style={S.starRow}>
                      {[1, 2, 3, 4, 5].map(n => (
                        <span key={n} onClick={() => setReviewRating(n)}
                          style={{ cursor: "pointer", fontSize: 24, color: n <= reviewRating ? "#f59e0b" : "#d1d5db" }}>
                          ★
                        </span>
                      ))}
                    </div>
                  </div>
                  <textarea
                    placeholder="Напишите ваш отзыв..."
                    value={reviewText}
                    onChange={e => setReviewText(e.target.value)}
                    style={S.reviewTextarea}
                    rows={3}
                  />
                  <button onClick={submitReview} style={S.reviewSubmitBtn}>
                    Отправить отзыв
                  </button>
                </div>

                {/* Список отзывов */}
                {reviews.length === 0 ? (
                  <p style={S.noReviews}>Пока нет отзывов. Будьте первым!</p>
                ) : (
                  reviews.map(r => (
                    <div key={r.id} style={S.reviewCard}>
                      <div style={S.reviewCardHeader}>
                        <div>
                          <span style={S.reviewUser}>{r.user_name}</span>
                          <span style={S.reviewDate}>{r.created_at}</span>
                        </div>
                        <div style={S.reviewStars}>
                          {[1, 2, 3, 4, 5].map(n => (
                            <span key={n} style={{ color: n <= r.rating ? "#f59e0b" : "#d1d5db", fontSize: 16 }}>★</span>
                          ))}
                        </div>
                      </div>
                      <p style={S.reviewText}>{r.text}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        )}

        {/* ======== РЕКОМЕНДАЦИИ ======== */}
        {page === "recommend" && (<div>
          <PageHead title="Рекомендации для вас" sub="Санатории отсортированы по степени соответствия вашим предпочтениям (метод Weighted Goal Programming)" />
          {results.length === 0 ? (
            <Empty icon="📝" text="Заполните профиль для получения персональных рекомендаций">
              <button onClick={() => setPage("profile")} style={S.primaryBtn}>Заполнить профиль</button>
            </Empty>
          ) : results.map((s, i) => (
            <div key={s.id} onClick={() => openDetail(s, "recommend")} style={{
              ...S.card, cursor: "pointer",
              borderLeft: i === 0 ? "4px solid #22c55e" : i === 1 ? "4px solid #3b82f6" : i === 2 ? "4px solid #f59e0b" : "4px solid transparent"
            }}>
              <div style={{ display: "flex", gap: 16 }}>
                <img src={getSanatoriumImage(s.id)} alt={s.name} style={S.cardImage} />
                <div style={{ flex: 1 }}>
                  <div style={S.cardHeader}>
                    <div><span style={S.rank}>#{i + 1}</span><span style={S.cardName}>{s.name}</span></div>
                    <div style={S.scoreBox}><span style={S.scoreLabel}>Score</span><span style={S.scoreVal}>{s.score}</span></div>
                  </div>
                  <div style={S.cardInfo}>
                    <Inf icon="💰" t={`${s.budget.toLocaleString()} ₽/сутки`} />
                    <Inf icon="📍" t={s.region} /><Inf icon="⭐" t={`${s.rating}`} /><Inf icon="🍽️" t={s.food} />
                  </div>
                  <div style={S.tagList}>
                    {s.tags && s.tags.slice(0, 6).map(t => (
                      <span key={t.id} style={{ ...S.tagBadge,
                        background: t.category === "medical" ? "#eff6ff" : t.category === "services" ? "#f0fdf4" : "#fff7ed",
                        color: t.category === "medical" ? "#1d4ed8" : t.category === "services" ? "#15803d" : "#c2410c"
                      }}>{t.name}</span>
                    ))}
                    {s.tags && s.tags.length > 6 && <span style={S.tagBadge}>+{s.tags.length - 6}</span>}
                  </div>
                </div>
              </div>
              <div style={S.cardFooter}>
                <button onClick={e => { e.stopPropagation(); toggleCompare(s.id); }}
                  style={compareIds.includes(s.id) ? S.compareActiveBtn : S.compareBtn}>
                  {compareIds.includes(s.id) ? "✓ В сравнении" : "Сравнить"}
                </button>
                <span style={S.clickHint}>Нажмите для подробностей →</span>
              </div>
            </div>
          ))}
        </div>)}

        {/* ======== ПРОФИЛЬ ======== */}
        {page === "profile" && (<div>
          <PageHead title="Настройки профиля" sub="Укажите ваши предпочтения для подбора санатория" />

          <div style={S.section}>
            <h3 style={S.secTitle}>Основные параметры</h3>
            <div style={S.formGrid}>
              <div style={S.formGroup}>
                <label style={S.label}>Цель отдыха</label>
                <select value={goal} onChange={e => setGoal(e.target.value)} style={S.select}>
                  <option value="отдых">Общий отдых</option><option value="лечение">Лечение</option>
                  <option value="профилактика">Профилактика</option><option value="реабилитация">Реабилитация</option>
                </select>
              </div>
              <div style={S.formGroup}>
                <label style={S.label}>Бюджет: <strong>{budget.toLocaleString()} ₽/сутки</strong></label>
                <input type="range" min="1000" max="20000" step="500" value={budget}
                  onChange={e => setBudget(Number(e.target.value))} style={S.slider} />
                <div style={S.rangeLabels}><span>1 000 ₽</span><span>20 000 ₽</span></div>
              </div>
              <div style={S.formGroup}>
                <label style={S.label}>Предпочитаемый регион</label>
                <select value={region} onChange={e => setRegion(e.target.value)} style={S.select}>
                  <option value="">Любой регион</option>
                  {getRegions().map(r => <option key={r} value={r}>{r}</option>)}
                </select>
              </div>
            </div>
          </div>

          <div style={S.section}>
            <h3 style={S.secTitle}>Приоритеты критериев</h3>
            <p style={S.hint}>Чем выше значение — тем важнее этот критерий при подборе</p>
            <div style={S.weightsGrid}>
              <WSlider l="💰 Бюджет" v={budgetWeight} o={setBudgetWeight} />
              <WSlider l="📍 Регион" v={regionWeight} o={setRegionWeight} />
              <WSlider l="🏥 Медицина" v={medicalWeight} o={setMedicalWeight} />
              <WSlider l="🛎️ Услуги" v={servicesWeight} o={setServicesWeight} />
              <WSlider l="🏠 Условия" v={conditionsWeight} o={setConditionsWeight} />
            </div>
          </div>

          <TagSection title="🏥 Медицинский профиль" tags={tags} cat="medical" sel={selectedTags} toggle={toggleTag} color="#3b82f6" />
          <TagSection title="🛎️ Услуги" tags={tags} cat="services" sel={selectedTags} toggle={toggleTag} color="#22c55e" />
          <TagSection title="🏠 Условия проживания" tags={tags} cat="conditions" sel={selectedTags} toggle={toggleTag} color="#f59e0b" />

          <div style={{ textAlign: "center", marginTop: 30 }}>
            <button onClick={saveProfile} style={S.primaryBtn}>💾 Сохранить и получить рекомендации</button>
          </div>
        </div>)}

        {/* ======== КАТАЛОГ ======== */}
        {page === "catalog" && (<div>
          <PageHead title="Каталог санаториев" sub={`Все санатории в нашей базе (${catalog.length})`} />
          <div style={S.catalogGrid}>
            {catalog.map(s => (
              <div key={s.id} style={S.catalogCard} onClick={() => openDetail(s, "catalog")}>
                <img src={getSanatoriumImage(s.id)} alt={s.name} style={S.catalogImage} />
                <div style={{ padding: "12px 0 0 0" }}>
                  <div style={S.catalogTop}><h3 style={S.catalogName}>{s.name}</h3><span style={S.ratingBadge}>⭐ {s.rating}</span></div>
                  <p style={S.catalogRegion}>📍 {s.region}</p>
                  <p style={S.catalogBudget}>💰 {s.budget.toLocaleString()} ₽/сутки</p>
                  <p style={S.catalogFood}>🍽️ {s.food}</p>
                  <div style={S.tagList}>
                    {s.tags && s.tags.slice(0, 5).map(t => <span key={t.id} style={S.smallTag}>{t.name}</span>)}
                    {s.tags && s.tags.length > 5 && <span style={S.smallTag}>+{s.tags.length - 5}</span>}
                  </div>
                  <div style={{ marginTop: 12, display: "flex", gap: 8, alignItems: "center" }}>
                    <button onClick={e => { e.stopPropagation(); toggleCompare(s.id); }}
                      style={compareIds.includes(s.id) ? S.compareActiveBtn : S.compareBtn}>
                      {compareIds.includes(s.id) ? "✓ В сравнении" : "⚖️ Сравнить"}
                    </button>
                    <span style={S.clickHint}>Подробнее →</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>)}

        {page === "settings" && (
          <div>
            <PageHead title="Настройки аккаунта" sub="Управление паролем и данными аккаунта" />
            <div style={S.section}>
              <h3 style={S.secTitle}>🔑 Смена пароля</h3>

              {passwordMsg && (
                <div style={{
                  padding: "10px 14px", borderRadius: 8, marginBottom: 16, fontSize: 14, textAlign: "center",
                  background: passwordMsg.includes("изменён") ? "#f0fdf4" : "#fef2f2",
                  color: passwordMsg.includes("изменён") ? "#16a34a" : "#dc2626"
                }}>
                  {passwordMsg}
                </div>
              )}

              <div style={{ maxWidth: 400 }}>
                <div style={S.formGroup}>
                  <label style={S.label}>Старый пароль</label>
                  <input type="password" value={oldPassword}
                    onChange={e => setOldPassword(e.target.value)}
                    placeholder="Введите текущий пароль"
                    style={S.authInput} />
                </div>
                <div style={S.formGroup}>
                  <label style={S.label}>Новый пароль</label>
                  <input type="password" value={newPassword}
                    onChange={e => setNewPassword(e.target.value)}
                    placeholder="Введите новый пароль"
                    style={S.authInput} />
                </div>
                <button onClick={() => {
                  if (!oldPassword || !newPassword) {
                    setPasswordMsg("Заполните оба поля");
                    return;
                  }
                  fetch(`${API}/api/password`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                      user_id: user.id,
                      old_password: oldPassword,
                      new_password: newPassword
                    })
                  })
                    .then(r => r.json())
                    .then(d => {
                      if (d.error) {
                        setPasswordMsg(d.error);
                      } else {
                        setPasswordMsg("Пароль успешно изменён");
                        setOldPassword("");
                        setNewPassword("");
                      }
                    });
                }} style={S.primaryBtn}>
                  Сменить пароль
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ======== СРАВНЕНИЕ ======== */}
        {page === "compare" && (<div>
          <PageHead title="Сравнение санаториев" sub="Сравните характеристики выбранных санаториев бок о бок" />
          {compareIds.length === 0 ? (
            <Empty icon="⚖️" text="Добавьте санатории для сравнения из каталога или рекомендаций">
              <button onClick={() => setPage("catalog")} style={S.primaryBtn}>Перейти в каталог</button>
            </Empty>
          ) : (
            <div style={S.compareGrid}>
              {compareIds.map(id => { const s = catalog.find(x => x.id === id); if (!s) return null; return (
                <div key={s.id} style={S.compareCard}>
                  <button onClick={() => toggleCompare(s.id)} style={S.removeBtn}>✕</button>
                  <img src={getSanatoriumImage(s.id)} alt={s.name} style={S.compareImage} />
                  <h3 style={S.compareName}>{s.name}</h3>
                  <CRow l="Регион" v={s.region} /><CRow l="Цена" v={`${s.budget.toLocaleString()} ₽/сут`} />
                  <CRow l="Рейтинг" v={`⭐ ${s.rating}`} /><CRow l="Питание" v={s.food} />
                  <h4 style={S.cTagTitle}>Медицина:</h4>
                  <div style={S.tagList}>{s.tags && s.tags.filter(t => t.category === "medical").map(t => <span key={t.id} style={S.smallTag}>{t.name}</span>)}</div>
                  <h4 style={S.cTagTitle}>Услуги:</h4>
                  <div style={S.tagList}>{s.tags && s.tags.filter(t => t.category === "services").map(t => <span key={t.id} style={S.smallTag}>{t.name}</span>)}</div>
                  <h4 style={S.cTagTitle}>Условия:</h4>
                  <div style={S.tagList}>{s.tags && s.tags.filter(t => t.category === "conditions").map(t => <span key={t.id} style={S.smallTag}>{t.name}</span>)}</div>
                </div>
              ); })}
            </div>
          )}
        </div>)}

      </main>
    </div>
  );
}

// ============================================================
// Аутентификация
// ============================================================
function AuthScreen({ onLogin }) {
  const [isReg, setIsReg] = useState(false);
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function doLogin() {
    setError("");
    fetch(`${API}/api/login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ login, password }) })
      .then(r => r.json()).then(d => d.error ? setError(d.error) : onLogin(d));
  }

  function doRegister() {
    setError(""); setSuccess("");
    fetch(`${API}/api/register`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name, login, password }) })
      .then(r => r.json()).then(d => d.error ? setError(d.error) : (setSuccess("Аккаунт создан! Войдите."), setIsReg(false)));
  }

  return (
    <div style={S.authWrap}><div style={S.authCard}>
      <h1 style={S.authLogo}>🏥 Подбор Санатория</h1>
      <p style={S.authSub}>Подберём санаторий по вашим предпочтениям</p>
      {error && <div style={S.errBox}>{error}</div>}
      {success && <div style={S.sucBox}>{success}</div>}
      {isReg ? (<div>
        <h2 style={S.authTitle}>Регистрация</h2>
        <input placeholder="Имя" value={name} onChange={e => setName(e.target.value)} style={S.authInput} />
        <input placeholder="Логин" value={login} onChange={e => setLogin(e.target.value)} style={S.authInput} />
        <input placeholder="Пароль" type="password" value={password} onChange={e => setPassword(e.target.value)} style={S.authInput} />
        <button onClick={doRegister} style={S.authBtn}>Зарегистрироваться</button>
        <p style={S.authSwitch}>Уже есть аккаунт? <span onClick={() => { setIsReg(false); setError(""); }} style={S.authLink}>Войти</span></p>
      </div>) : (<div>
        <h2 style={S.authTitle}>Вход</h2>
        <input placeholder="Логин" value={login} onChange={e => setLogin(e.target.value)} style={S.authInput} />
        <input placeholder="Пароль" type="password" value={password} onChange={e => setPassword(e.target.value)} style={S.authInput} onKeyDown={e => e.key === "Enter" && doLogin()} />
        <button onClick={doLogin} style={S.authBtn}>Войти</button>
        <p style={S.authSwitch}>Нет аккаунта? <span onClick={() => { setIsReg(true); setError(""); }} style={S.authLink}>Зарегистрироваться</span></p>
      </div>)}
    </div></div>
  );
}

// ============================================================
// Миникомпоненты
// ============================================================
function NavBtn({ a, o, children }) {
  return <button onClick={o} style={{ ...S.navBtn, background: a ? "#1e40af" : "transparent", color: a ? "white" : "#94a3b8" }}>{children}</button>;
}
function WSlider({ l, v, o }) {
  return <div style={S.weightItem}><div style={S.weightHeader}><span>{l}</span><span style={S.weightVal}>{v}</span></div><input type="range" min="1" max="10" value={v} onChange={e => o(Number(e.target.value))} style={S.slider} /></div>;
}
function TagChip({ tag, selected, onClick, color }) {
  return <button onClick={onClick} style={{ padding: "8px 16px", borderRadius: 20, border: selected ? `2px solid ${color}` : "1px solid #d1d5db", background: selected ? `${color}15` : "white", color: selected ? color : "#374151", cursor: "pointer", fontSize: 14, fontWeight: selected ? 600 : 400 }}>{selected ? "✓ " : ""}{tag.name}</button>;
}
function Inf({ icon, t }) { return <span style={S.infoBadge}>{icon} {t}</span>; }
function PageHead({ title, sub }) { return <div style={S.pageHeader}><h2 style={S.pageTitle}>{title}</h2><p style={S.pageSub}>{sub}</p></div>; }
function Empty({ icon, text, children }) { return <div style={S.empty}><p style={S.emptyIcon}>{icon}</p><p style={S.emptyText}>{text}</p>{children}</div>; }
function CRow({ l, v }) { return <div style={S.cRow}><span style={S.cLabel}>{l}</span><span style={S.cValue}>{v}</span></div>; }
function TagSection({ title, tags, cat, sel, toggle, color }) {
  return <div style={S.section}><h3 style={S.secTitle}>{title}</h3><div style={S.tagGrid}>{tags.filter(t => t.category === cat).map(tag => <TagChip key={tag.id} tag={tag} selected={sel.includes(tag.id)} onClick={() => toggle(tag.id)} color={color} />)}</div></div>;
}
function DetailInfo({ icon, label, value }) {
  return <div style={S.detailInfoItem}><span style={{ fontSize: 28 }}>{icon}</span><div><span style={S.detailInfoLabel}>{label}</span><span style={S.detailInfoValue}>{value}</span></div></div>;
}
function DetailTagSection({ title, tags, cat, bg, fg }) {
  const filtered = tags ? tags.filter(t => t.category === cat) : [];
  return <div style={S.detailSection}><h3 style={S.detailSecTitle}>{title}</h3><div style={S.tagList}>{filtered.length > 0 ? filtered.map(t => <span key={t.id} style={{ ...S.detailTag, background: bg, color: fg }}>{t.name}</span>) : <span style={{ fontSize: 14, color: "#94a3b8", fontStyle: "italic" }}>Нет данных</span>}</div></div>;
}

// ============================================================
// СТИЛИ
// ============================================================
const S = {
  app: { minHeight: "100vh", background: "#f1f5f9", fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif", color: "#1e293b" },
  header: { background: "#0f172a", padding: "0 20px", position: "sticky", top: 0, zIndex: 100, boxShadow: "0 2px 8px rgba(0,0,0,0.15)" },
  headerInner: { maxWidth: 1100, margin: "0 auto", display: "flex", alignItems: "center", height: 60, gap: 20 },
  logo: { color: "white", margin: 0, fontSize: 18, whiteSpace: "nowrap" },
  nav: { display: "flex", gap: 4, flex: 1 },
  navBtn: { border: "none", padding: "8px 14px", borderRadius: 8, cursor: "pointer", fontSize: 14, fontWeight: 500 },
  userBlock: { display: "flex", alignItems: "center", gap: 12 },
  userName: { color: "#94a3b8", fontSize: 14 },
  logoutBtn: { background: "#ef4444", color: "white", border: "none", padding: "6px 14px", borderRadius: 6, cursor: "pointer", fontSize: 13 },
  main: { maxWidth: 1100, margin: "0 auto", padding: "30px 20px" },
  pageHeader: { marginBottom: 30 },
  pageTitle: { margin: "0 0 8px 0", fontSize: 28, fontWeight: 700, color: "#0f172a" },
  pageSub: { margin: 0, fontSize: 15, color: "#64748b" },
  empty: { textAlign: "center", padding: "60px 20px", background: "white", borderRadius: 12, border: "1px solid #e2e8f0" },
  emptyIcon: { fontSize: 48, margin: "0 0 10px 0" },
  emptyText: { fontSize: 16, color: "#64748b", margin: "0 0 20px 0" },
  card: { background: "white", borderRadius: 12, padding: 20, marginBottom: 12, border: "1px solid #e2e8f0", boxShadow: "0 1px 3px rgba(0,0,0,0.04)" },
  cardImage: { width: 160, height: 100, objectFit: "cover", borderRadius: 8, flexShrink: 0 },
  cardHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  rank: { fontSize: 22, fontWeight: 700, color: "#3b82f6", marginRight: 10 },
  cardName: { fontSize: 20, fontWeight: 600 },
  scoreBox: { textAlign: "center", background: "#f8fafc", padding: "6px 16px", borderRadius: 10, border: "1px solid #e2e8f0" },
  scoreLabel: { display: "block", fontSize: 11, color: "#94a3b8", textTransform: "uppercase" },
  scoreVal: { fontSize: 18, fontWeight: 700, color: "#0f172a" },
  cardBody: { marginBottom: 12 },
  cardInfo: { display: "flex", flexWrap: "wrap", gap: 10, marginBottom: 8 },
  infoBadge: { fontSize: 14, color: "#475569", background: "#f8fafc", padding: "4px 10px", borderRadius: 6 },
  tagList: { display: "flex", flexWrap: "wrap", gap: 5 },
  tagBadge: { padding: "3px 10px", borderRadius: 12, fontSize: 12, fontWeight: 500 },
  cardFooter: { borderTop: "1px solid #f1f5f9", paddingTop: 12, marginTop: 12, display: "flex", gap: 8, alignItems: "center" },
  clickHint: { fontSize: 13, color: "#94a3b8", marginLeft: "auto" },
  primaryBtn: { background: "#2563eb", color: "white", border: "none", padding: "12px 28px", borderRadius: 8, fontSize: 16, fontWeight: 600, cursor: "pointer" },
  compareBtn: { background: "white", color: "#475569", border: "1px solid #d1d5db", padding: "6px 14px", borderRadius: 6, fontSize: 13, cursor: "pointer" },
  compareActiveBtn: { background: "#2563eb", color: "white", border: "1px solid #2563eb", padding: "6px 14px", borderRadius: 6, fontSize: 13, cursor: "pointer" },
  section: { background: "white", borderRadius: 12, padding: 24, marginBottom: 16, border: "1px solid #e2e8f0" },
  secTitle: { margin: "0 0 16px 0", fontSize: 18, fontWeight: 600 },
  hint: { margin: "-8px 0 16px 0", fontSize: 13, color: "#94a3b8" },
  formGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 },
  formGroup: { display: "flex", flexDirection: "column" },
  label: { fontSize: 14, color: "#475569", marginBottom: 6 },
  select: { padding: "10px 12px", borderRadius: 8, border: "1px solid #d1d5db", fontSize: 14, background: "white" },
  slider: { width: "100%", accentColor: "#2563eb" },
  rangeLabels: { display: "flex", justifyContent: "space-between", fontSize: 12, color: "#94a3b8", marginTop: 4 },
  weightsGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 },
  weightItem: { padding: 12, background: "#f8fafc", borderRadius: 8 },
  weightHeader: { display: "flex", justifyContent: "space-between", marginBottom: 6, fontSize: 14 },
  weightVal: { fontWeight: 700, color: "#2563eb", fontSize: 16 },
  tagGrid: { display: "flex", flexWrap: "wrap", gap: 8 },
  // Каталог
  catalogGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: 16 },
  catalogCard: { background: "white", borderRadius: 12, overflow: "hidden", border: "1px solid #e2e8f0", cursor: "pointer" },
  catalogImage: { width: "100%", height: 160, objectFit: "cover" },
  catalogTop: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  catalogName: { margin: 0, fontSize: 17, fontWeight: 600 },
  ratingBadge: { background: "#fef3c7", padding: "4px 10px", borderRadius: 12, fontSize: 13, fontWeight: 600 },
  catalogRegion: { margin: "0 0 4px 0", fontSize: 14, color: "#475569" },
  catalogBudget: { margin: "0 0 4px 0", fontSize: 14, fontWeight: 600, color: "#0f172a" },
  catalogFood: { margin: "0 0 10px 0", fontSize: 13, color: "#64748b" },
  smallTag: { padding: "2px 8px", background: "#f1f5f9", borderRadius: 8, fontSize: 11, color: "#475569" },
  // Сравнение
  compareGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16, alignItems: "start" },
  compareCard: { background: "white", borderRadius: 12, overflow: "hidden", border: "1px solid #e2e8f0", position: "relative" },
  compareImage: { width: "100%", height: 140, objectFit: "cover" },
  removeBtn: { position: "absolute", top: 10, right: 10, background: "rgba(255,255,255,0.9)", color: "#ef4444", border: "none", borderRadius: "50%", width: 28, height: 28, cursor: "pointer", fontWeight: 700, fontSize: 14, zIndex: 2 },
  compareName: { margin: "12px 16px 12px 16px", fontSize: 18, fontWeight: 600, paddingRight: 20 },
  cRow: { display: "flex", justifyContent: "space-between", padding: "8px 16px", borderBottom: "1px solid #f1f5f9", fontSize: 14 },
  cLabel: { color: "#64748b" },
  cValue: { fontWeight: 600, color: "#0f172a" },
  cTagTitle: { margin: "12px 16px 6px 16px", fontSize: 13, color: "#64748b", fontWeight: 600 },
  // Детальный просмотр
  backBtn: { background: "white", border: "1px solid #d1d5db", padding: "8px 16px", borderRadius: 8, cursor: "pointer", fontSize: 14, color: "#475569", marginBottom: 20, display: "inline-block" },
  detailImageWrap: { position: "relative", borderRadius: "16px 16px 0 0", overflow: "hidden", marginBottom: 0 },
  detailImage: { width: "100%", height: 280, objectFit: "cover", display: "block" },
  detailImageOverlay: { position: "absolute", bottom: 0, left: 0, right: 0, background: "linear-gradient(transparent, rgba(0,0,0,0.7))", padding: "40px 32px 20px 32px" },
  detailImageName: { margin: "0 0 4px 0", fontSize: 32, fontWeight: 700, color: "white" },
  detailImageRegion: { margin: 0, fontSize: 16, color: "rgba(255,255,255,0.85)" },
  detailCard: { background: "white", borderRadius: "0 0 16px 16px", padding: 32, border: "1px solid #e2e8f0", borderTop: "none", boxShadow: "0 4px 12px rgba(0,0,0,0.06)" },
  detailScoreBar: { display: "flex", justifyContent: "space-between", alignItems: "center", background: "#eff6ff", padding: "12px 20px", borderRadius: 10, marginBottom: 24, fontSize: 14, color: "#1e40af" },
  detailScoreVal: { fontWeight: 700, fontSize: 18 },
  detailGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 24 },
  detailInfoItem: { display: "flex", gap: 12, alignItems: "center", padding: 16, background: "#f8fafc", borderRadius: 10 },
  detailInfoLabel: { display: "block", fontSize: 12, color: "#94a3b8", marginBottom: 2 },
  detailInfoValue: { display: "block", fontSize: 16, fontWeight: 600, color: "#0f172a" },
  detailSection: { marginBottom: 20, paddingBottom: 20, borderBottom: "1px solid #f1f5f9" },
  detailSecTitle: { margin: "0 0 12px 0", fontSize: 16, fontWeight: 600 },
  detailTag: { padding: "6px 14px", borderRadius: 16, fontSize: 13, fontWeight: 500 },
  // Отзывы
  reviewsSection: { marginTop: 32, paddingTop: 24, borderTop: "2px solid #e2e8f0" },
  reviewsTitle: { margin: "0 0 20px 0", fontSize: 20, fontWeight: 600 },
  reviewForm: { background: "#f8fafc", borderRadius: 12, padding: 20, marginBottom: 24 },
  reviewFormHeader: { display: "flex", alignItems: "center", gap: 12, marginBottom: 12 },
  reviewFormLabel: { fontSize: 14, color: "#475569" },
  starRow: { display: "flex", gap: 2 },
  reviewTextarea: { width: "100%", padding: 12, borderRadius: 8, border: "1px solid #d1d5db", fontSize: 14, fontFamily: "inherit", resize: "vertical", boxSizing: "border-box" },
  reviewSubmitBtn: { marginTop: 12, background: "#2563eb", color: "white", border: "none", padding: "10px 24px", borderRadius: 8, fontSize: 14, fontWeight: 600, cursor: "pointer" },
  noReviews: { fontSize: 14, color: "#94a3b8", fontStyle: "italic", textAlign: "center", padding: 20 },
  reviewCard: { background: "white", border: "1px solid #e2e8f0", borderRadius: 10, padding: 16, marginBottom: 10 },
  reviewCardHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  reviewUser: { fontWeight: 600, fontSize: 14, color: "#0f172a", marginRight: 10 },
  reviewDate: { fontSize: 12, color: "#94a3b8" },
  reviewStars: { display: "flex", gap: 1 },
  reviewText: { margin: 0, fontSize: 14, color: "#334155", lineHeight: 1.5 },
  // Аутентификация
  authWrap: { minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)", fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif" },
  authCard: { background: "white", padding: "40px", borderRadius: 16, width: 380, boxShadow: "0 20px 60px rgba(0,0,0,0.3)" },
  authLogo: { textAlign: "center", fontSize: 22, margin: "0 0 4px 0", color: "#0f172a" },
  authSub: { textAlign: "center", fontSize: 14, color: "#64748b", margin: "0 0 24px 0" },
  authTitle: { fontSize: 20, fontWeight: 600, margin: "0 0 16px 0", textAlign: "center" },
  authInput: { display: "block", width: "100%", padding: "12px 14px", marginBottom: 12, borderRadius: 8, border: "1px solid #d1d5db", fontSize: 15, boxSizing: "border-box" },
  authBtn: { display: "block", width: "100%", padding: "12px", background: "#2563eb", color: "white", border: "none", borderRadius: 8, fontSize: 16, fontWeight: 600, cursor: "pointer", marginTop: 8 },
  authSwitch: { textAlign: "center", fontSize: 14, color: "#64748b", marginTop: 16 },
  authLink: { color: "#2563eb", cursor: "pointer", fontWeight: 600 },
  errBox: { background: "#fef2f2", color: "#dc2626", padding: "10px 14px", borderRadius: 8, marginBottom: 16, fontSize: 14, textAlign: "center" },
  sucBox: { background: "#f0fdf4", color: "#16a34a", padding: "10px 14px", borderRadius: 8, marginBottom: 16, fontSize: 14, textAlign: "center" },
};
