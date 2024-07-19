import React, { useState } from 'react';

const FileUploader = () => {
    const [file, setFile] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;

        setIsLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/audio/convert', {
                method: 'POST',
                body: formData,
                headers: {
                    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const text = await response.text();
            const lines = text.trim().split('\n');
            const result = lines.map(line => JSON.parse(line));

            window.dispatchEvent(new CustomEvent('transcriptionResult', { detail: result }));
        } catch (error) {
            console.error('Error during file upload or data parsing:', error);
            // 在这里处理错误，例如显示错误消息给用户
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-md mx-auto">
            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="flex items-center justify-center w-full">
                    <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                        <div className="flex flex-col items-center justify-center pt-5 pb-6">
                            <svg className="w-8 h-8 mb-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                            </svg>
                            <p className="mb-1 text-sm text-gray-500"><span className="font-semibold">点击上传</span> 或拖放文件</p>
                            <p className="text-xs text-gray-500">支持 WAV, MP3 或 M4A 格式</p>
                        </div>
                        <input id="dropzone-file" type="file" className="hidden" onChange={handleFileChange} accept="audio/*" />
                    </label>
                </div>
                {file && (
                    <p className="text-sm text-gray-500 text-center">
                        已选择文件: {file.name}
                    </p>
                )}
                <button
                    type="submit"
                    className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 transition duration-150 ease-in-out"
                    disabled={!file || isLoading}
                >
                    {isLoading ? (
                        <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              转录中...
            </span>
                    ) : '开始转录'}
                </button>
            </form>
        </div>
    );
};

export default FileUploader;