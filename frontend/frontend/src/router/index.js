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
import LightCard from "@/components/LightCard.vue";
import AddBookForm from "@/components/AddBookForm.vue";
import EditBookForm from "@/components/EditBookForm.vue";
import MonitorTable from "@/components/MonitorTable.vue";
import CardDetails from "@/components/CardDetails.vue";
import UserDetail from "@/components/UserDetail.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/userdetail",
    name: "UserDetail",
    component: UserDetail,
  },
  {
    path: "/viewall",
    name: "ViewAll",
    component: ViewAll,
  },
  {
    path: "/carddetails/:id",
    name: "CardDetails",
    component: CardDetails,
    props: true,
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
  {
    path: "/light-card",
    name: "LightCard",
    component: LightCard,
  },
  {
    path: "/add-book",
    name: "AddBookForm",
    component: AddBookForm,
  },
  {
    path: "/edit-book",
    name: "EditBookForm",
    component: EditBookForm,
  },
  {
    path: "/monitor",
    name: "MonitorTable",
    component: MonitorTable,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
