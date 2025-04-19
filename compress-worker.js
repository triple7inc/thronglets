importScripts("https://cdn.jsdelivr.net/npm/pako@2.1.0/dist/pako.min.js")
onmessage=e=>{
    try{
        let json=JSON.stringify(e.data)
        let compressed=pako.deflate(json)
        postMessage(compressed)
    }catch(err){
        postMessage({error:err.message})
    }
}