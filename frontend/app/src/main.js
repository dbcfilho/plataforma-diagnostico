import { createApp } from 'vue'
import App from './App.vue'

// 1. IMPORTA A CONFIGURAÇÃO DO ROUTER
// Esta linha traz o arquivo de rotas que você criou.
import router from './router'

// 2. IMPORTA O CSS GLOBAL DO TAILWIND
import './index.css'

// Cria a instância principal do Vue a partir do componente App.vue
const app = createApp(App)

// 3. INSTALA O ROUTER NA APLICAÇÃO
// Esta é a linha mais importante. Ela "ensina" o Vue sobre o <router-view>
// e todas as outras funcionalidades de roteamento.
app.use(router)

// 4. "MONTA" A APLICAÇÃO NO HTML
// Renderiza tudo na <div id="app"> do seu index.html
app.mount('#app')