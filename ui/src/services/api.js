import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

const baseUrl = "http://127.0.0.1/api"

export const pixSmushApi = createApi({
    reducerPath: "pixSmushApi",
    baseQuery: fetchBaseQuery({ baseUrl }),
    endpoints: (builder) => ({
        compressImage: builder.mutation({
            query: (file) => ({
                url: "/images/compress",
                method: "POST",
                body: file,
            }),
        }),
        downloadImage: builder.query({
            query: (imageId) => `/download/${imageId}`,
        }),
        getAllImages: builder.query({
            query: () => "/images",
        }),
    }),
})

export const { useCompressImageMutation, useDownloadImageQuery, useGetAllImagesQuery } = pixSmushApi