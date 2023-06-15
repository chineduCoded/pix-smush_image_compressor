import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

const baseUrl = "http://127.0.0.1:5000/"

export const pixSmushApi = createApi({
    reducerPath: "pixSmushApi",
    baseQuery: fetchBaseQuery({ baseUrl }),
    tagTypes: ['Images'],
    endpoints: (builder) => ({
        compressImage: builder.mutation({
            query: (imageData) => ({
                url: "api/images/compress",
                method: "POST",
                body: imageData,
            }),
            invalidatesTags: ['Images'],
        }),
        downloadImage: builder.query({
            query: (id) => `api/download/${id}`,
            transformResponse: (response) => response.blob(),
            providesTags: ['Images'],
        }),
        getAllImages: builder.query({
            query: () => "api/images",
            providesTags: ['Images'],
        }),
    }),
})

export const { useCompressImageMutation, useDownloadImageQuery, useGetAllImagesQuery } = pixSmushApi