import { createRouter, createWebHistory } from \"vue-router\";
import { useAuthStore } from \"../stores/auth\"; // Importar store para o guard

const routes = [
  {
    path: \"/login\",
    name: \"Login\",
    component: () => import(\"../views/LoginView.vue\"),
    meta: { requiresAuth: false }
  },
  {
    path: \"/\",
    name: \"Dashboard\",
    component: () => import(\"../views/DashboardView.vue\"),
    meta: { requiresAuth: true }
  },
  {
    path: \"/admin\",
    name: \"AdminPanel\",
    component: () => import(\"../views/AdminPanelView.vue\"),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: \"/professor\", // Rota para a área do professor
    name: \"TeacherPanel\",
    component: () => import(\"../views/TeacherPanelView.vue\"),
    meta: { requiresAuth: true } // Requer apenas autenticação
  },
  {
    path: \"/:pathMatch(.*)*\",
    name: \"NotFound\",
    component: () => import(\"../views/NotFoundView.vue\")
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();
  if (!auth.token) {
      auth.initialize();
  }

  const isAuthenticated = auth.isAuthenticated;
  // Assumindo que a store tem uma forma de identificar se o usuário é professor ou admin
  // Exemplo: const isTeacher = auth.isTeacher; 
  const isAdminUser = auth.isAdmin;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: \"Login\", query: { redirect: to.fullPath } });
  } else if (to.meta.requiresAdmin && !isAdminUser) {
    console.warn(\"Acesso não autorizado à rota admin.\");
    next({ name: \"Dashboard\" }); 
  } 
  // Adicionar verificação para rota de professor se necessário (ex: só professor acessa /professor)
  // else if (to.name === \"TeacherPanel\" && !isTeacher) {
  //   next({ name: \"Dashboard\" });
  // }
  else if (to.name === \"Login\" && isAuthenticated) {
    next({ name: \"Dashboard\" });
  } else {
    next();
  }
});

export default router;

