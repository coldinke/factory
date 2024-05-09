import { createApp } from "vue";
import App from "./App.vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import router from "./config/router";

const app = createApp(App);

app.use(router).use(ElementPlus).mount("#app");