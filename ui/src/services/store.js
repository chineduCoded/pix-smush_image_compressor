import { configureStore } from "@reduxjs/toolkit"
import { setupListeners } from "@reduxjs/toolkit/query"
import { pixSmushApi } from "./api"

export const store = configureStore({
    reducer: {
        [pixSmushApi.reducerPath]: pixSmushApi.reducer,
    },

    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(pixSmushApi.middleware),
})

setupListeners(store.dispatch)