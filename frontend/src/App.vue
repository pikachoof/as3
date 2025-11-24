<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app">
    <header class="app__header">
      <RouterLink class="app__logo" to="/">CareConnect</RouterLink>
      <nav class="app__nav">
        <RouterLink to="/caregivers">Caregivers</RouterLink>
        <RouterLink to="/families">Families</RouterLink>
        <RouterLink to="/jobs">Job Board</RouterLink>
        <RouterLink to="/appointments">Appointments</RouterLink>
        <RouterLink to="/messages">Messages</RouterLink>
      </nav>
    </header>
    <main class="app__main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f4f6fb;
}

.app__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  background: #214e8a;
  color: #fff;
}

.app__logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  text-decoration: none;
}

.app__nav {
  display: flex;
  gap: 1rem;
}

.app__nav a {
  color: #dce7f9;
  text-decoration: none;
  font-weight: 500;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
}

.app__nav a.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.app__main {
  flex: 1;
  padding: 2rem;
}

@media (max-width: 768px) {
  .app__header {
    flex-direction: column;
    align-items: flex-start;
  }

  .app__nav {
    flex-wrap: wrap;
    margin-top: 1rem;
    gap: 0.5rem;
  }
}
</style>
