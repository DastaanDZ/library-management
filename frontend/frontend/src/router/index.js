import LandingPage from "@/components/LandingPage.vue";
import LoginForm from "@/components/LoginForm.vue";
import RegisterForm from "@/components/RegisterForm.vue";
import Shark from "@/components/Shark.vue";
import UserInfo from "@/components/UserInfo.vue";
import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/shark",
    name: "Shark",
    component: Shark,
  },
  {
    path: "/register",
    name: "RegisterForm",
    component: RegisterForm,
  },
  {
    path: "/login",
    name: "LoginForm",
    component: LoginForm,
  },
  {
    path: "/user-info",
    name: "UserInfo",
    component: UserInfo,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
