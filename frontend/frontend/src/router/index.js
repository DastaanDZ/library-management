import LandingPage from "@/components/LandingPage.vue";
import LoginForm from "@/components/LoginForm.vue";
import RegisterForm from "@/components/RegisterForm.vue";
import Shark from "@/components/Shark.vue";
import Sidebar from "@/components/Sidebar.vue";
import UserEditForm from "@/components/UserEditForm.vue";
import UserInfo from "@/components/UserInfo.vue";
import Vue from "vue";
import VueRouter from "vue-router";
import ViewAll from "@/components/ViewAll.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/viewall",
    name: "ViewAll",
    component: ViewAll,
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
  {
    path: "/user-edit",
    name: "UserEditForm",
    component: UserEditForm,
  },
  {
    path: "/sidebar",
    name: "Sidebar",
    component: Sidebar,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
