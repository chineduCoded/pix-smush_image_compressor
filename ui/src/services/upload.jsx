
const removeFile = (filename) => {
    setFiles(files.filter(file => file.name !== filename))
}

const FileUpload = ({files, setFiles, removeFile}) => {
    const uploadhandler = (e) => {
        const file = e.target.files[0]
        file.isLoading = true
        setFiles([...files, file])

        // upload file
        const formData = new FormData()
        formData.append(file.name, file, file.name)

        // send to backend
        axios.post("url", formData)
        .then((res) => {
            file.isLoading = false,
            setFiles([...files, file])
        })
        .catch((err) => {
            console.error(err)
            removeFile(file)
        })
    }
}