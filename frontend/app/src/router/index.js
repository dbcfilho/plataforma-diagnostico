import { createRouter, createWebHistory } from "vue-router";
// A linha abaixo deve ser descomentada quando você criar sua store (Pinia)
// import { useAuthStore } from "../stores/auth";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/LoginView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: "/",
    name: "Dashboard",
    component: () => import("../views/DashboardView.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/admin",
    name: "AdminPanel",
    component: () => import("../views/AdminPanelView.vue"),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: "/professor",
    name: "TeacherPanel",
    component: () => import("../views/TeacherPanelView.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("../views/NotFoundView.vue")
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Lógica de proteção de rotas (Route Guard)
router.beforeEach((to, from, next) => {
  // Exemplo de verificação simples via localStorage.
  // Substitua pela sua lógica com a store (Pinia) quando estiver pronta.
  const isAuthenticated = !!localStorage.getItem('authToken');
  const userRole = localStorage.getItem('userRole'); // Ex: 'admin', 'teacher'

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Se a rota exige autenticação e o usuário não está logado, redireciona para o login.
    next({ name: "Login", query: { redirect: to.fullPath } });
  } else if (to.meta.requiresAdmin && userRole !== 'admin') {
    // Se a rota exige admin e o usuário não é admin, redireciona para o dashboard.
    console.warn("Acesso não autorizado à rota de admin.");
    next({ name: "Dashboard" });
  } else if (to.name === "Login" && isAuthenticated) {
    // Se o usuário já está logado e tenta acessar a página de login, redireciona para o dashboard.
    next({ name: "Dashboard" });
  } else {
    // Em todos os outros casos, permite o acesso.
    next();
  }
});

export default router;