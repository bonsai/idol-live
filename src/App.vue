<script setup>
import { computed, onMounted, ref } from 'vue'

const data = ref({ period: {}, events: [] })
const from = ref('2026-09-09')
const to = ref('2026-09-20')
const area = ref('')
const underBudget = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await fetch(`${import.meta.env.BASE_URL}.data/events.json`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    data.value = await response.json()
  } catch (e) {
    error.value = `データを読み込めませんでした: ${e.message}`
  }
})

const events = computed(() => [...(data.value.events ?? [])]
  .filter((event) => !area.value || event.area === area.value)
  .filter((event) => !underBudget.value || event.budget?.within_budget !== false)
  .filter((event) => !from.value || event.date >= from.value)
  .filter((event) => !to.value || event.date <= to.value)
  .sort((a, b) => `${a.date}${a.start_at ?? ''}`.localeCompare(`${b.date}${b.start_at ?? ''}`)))

const areas = computed(() => [...new Set((data.value.events ?? []).map((e) => e.area).filter(Boolean))])

const priceText = (event) => {
  const budget = event.budget
  if (!budget) return event.admission?.label || '料金要確認'
  if (budget.total_price != null) return `${budget.total_price.toLocaleString()}円${budget.drink_included ? '（ドリンク込）' : ''}`
  if (budget.admission_price === 0 && budget.drink_price == null) return '入場無料（料金要確認）'
  return event.admission?.label || '料金要確認'
}
</script>

<template>
  <main class="container">
    <header>
      <p class="eyebrow">IDOL LIVE</p>
      <h1>東京の低予算・フリーライブ</h1>
      <p class="lead">完全無料に限定せず、ドリンク込みで1,000円未満をゆるく発見。</p>
    </header>

    <section class="filters" aria-label="検索条件">
      <label>開始日<input v-model="from" type="date" /></label>
      <label>終了日<input v-model="to" type="date" /></label>
      <label>エリア<select v-model="area"><option value="">すべて</option><option v-for="item in areas" :key="item" :value="item">{{ item }}</option></select></label>
      <label class="check"><input v-model="underBudget" type="checkbox" /> 1,000円未満</label>
    </section>

    <p v-if="error" class="error">{{ error }}</p>
    <section class="summary">{{ events.length }}件 <span>·</span> {{ from }}〜{{ to }}</section>

    <section v-if="events.length" class="list">
      <article v-for="event in events" :key="event.id ?? `${event.date}-${event.title}`" class="card">
        <div class="date">{{ event.date }}</div>
        <div class="body">
          <h2>{{ event.title || 'ライブ' }}</h2>
          <p v-if="event.artists?.length" class="artists">{{ event.artists.join(' / ') }}</p>
          <p>{{ event.venue }}<span v-if="event.area"> · {{ event.area }}</span></p>
          <div class="badges">
            <span class="badge">{{ priceText(event) }}</span>
            <span v-if="event.free_status?.drink_required" class="badge muted">ドリンクあり</span>
            <span v-if="event.free_status?.reservation_required" class="badge muted">要予約</span>
            <span v-if="event.metadata?.confidence" class="badge muted">{{ event.metadata.confidence }}</span>
          </div>
          <p v-if="event.budget?.note" class="note">{{ event.budget.note }}</p>
          <a v-if="event.source_url" :href="event.source_url" target="_blank" rel="noopener">情報源 ↗</a>
        </div>
      </article>
    </section>
    <section v-else class="empty">
      <strong>該当するライブはありません</strong>
      <p>条件をゆるめるか、データを追加するとここに表示されます。</p>
    </section>

    <footer>data: JSON fixture · 料金・ドリンク・予約条件・確認日などのメタデータを保持</footer>
  </main>
</template>
