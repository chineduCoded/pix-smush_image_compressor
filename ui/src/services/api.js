import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

const baseUrl = "http://127.0.0.1:5000/api"

export const pixSmushApi = createApi({
    reducerPath: "pixSmushApi",
    baseQuery: fetchBaseQuery({ baseUrl }),
    tagTypes: ['Images'],
    endpoints: (builder) => ({
        compressImage: builder.mutation({
            query: (imageData) => ({
                url: "/images/compress",
                method: "POST",
                body: imageData,
            }),
            invalidatesTags: ['Images'],
        }),
        downloadImage: builder.query({
            query: (imageId) => `/download/${imageId}`,
            providesTags: ['Images'],
        }),
        getAllImages: builder.query({
            query: () => "/images",
            providesTags: ['Images'],
        }),
    }),
})

export const { useCompressImageMutation, useDownloadImageQuery, useGetAllImagesQuery } = pixSmushApi