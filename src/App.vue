<script setup>
import { computed, onMounted, ref } from 'vue'

const data = ref({ period: {}, events: [] })
const from = ref('2026-09-14')
const to = ref('2026-09-20')
const area = ref('')
const freeOnly = ref(true)
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
  .filter((event) => !freeOnly.value || event.free_status?.free === true)
  .filter((event) => !from.value || event.date >= from.value)
  .filter((event) => !to.value || event.date <= to.value)
  .sort((a, b) => `${a.date}${a.start_at ?? ''}`.localeCompare(`${b.date}${b.start_at ?? ''}`)))

const areas = computed(() => [...new Set((data.value.events ?? []).map((e) => e.area).filter(Boolean))])
</script>

<template>
  <main class="container">
    <header>
      <p class="eyebrow">IDOL LIVE</p>
      <h1>東京の無銭・フリーライブ</h1>
      <p class="lead">無料で行けるアイドルライブを、日付順にチェック。</p>
    </header>

    <section class="filters" aria-label="検索条件">
      <label>開始日<input v-model="from" type="date" /></label>
      <label>終了日<input v-model="to" type="date" /></label>
      <label>エリア<select v-model="area"><option value="">すべて</option><option v-for="item in areas" :key="item" :value="item">{{ item }}</option></select></label>
      <label class="check"><input v-model="freeOnly" type="checkbox" /> 完全無料</label>
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
            <span class="badge">{{ event.admission?.label || '無料' }}</span>
            <span v-if="event.free_status?.drink_required" class="badge muted">1Dあり</span>
            <span v-if="event.free_status?.reservation_required" class="badge muted">要予約</span>
          </div>
          <a v-if="event.source_url" :href="event.source_url" target="_blank" rel="noopener">情報源 ↗</a>
        </div>
      </article>
    </section>
    <section v-else class="empty">
      <strong>該当するライブはありません</strong>
      <p>条件をゆるめるか、データを追加するとここに表示されます。</p>
    </section>

    <footer>data: JSON fixture · fetched_at を含む一次データを正規データとして利用</footer>
  </main>
</template>
