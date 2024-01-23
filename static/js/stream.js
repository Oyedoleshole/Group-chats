const APP_ID = '20f638f7c0a34553b60f309b32a396f0'
const CHANNEL = sessionStorage.getItem('room')
const TOKEN = sessionStorage.getItem('token')
let UID = sessionStorage.getItem('UID');
let NAME = sessionStorage.getItem('name')
const client = AgoraRTC.createClient({mode:'rtc',codec:'vp8'})

let localsTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL
    client.on('user-published',handleUser)
    client.on('user-left', handleUserLeft)
    try{
        await client.join(APP_ID, CHANNEL, TOKEN, UID)
    }catch(error){
        console.error(error)
    }
    localsTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
    let member = await createMember()
    let player =`<div  class="video-container" id="user-container-${UID}">
                    <div class="video-player" id="user-${UID}"></div>
                    <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                </div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend',player)
    localsTracks[1].play(`user-${UID}`)
    await client.publish([localsTracks[0],localsTracks[1]])
}
let handleUser = async (user, mediaType) => {
    remoteUsers[user.uid]=user
    await client.subscibe(user, mediaType)

    if (mediaType === 'video'){
        let player = document.getElementById(`user-container${user.uid}`)
        if (player != null){
            player.remove()
        }
        let member = await getMembers()
        player = `<div  class="video-container" id="user-container-${user.uid}">
                    <div class="video-player" id="user-${user.uid}"></div>
                    <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                </div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend',player)
        user.videoTrack.play(`user-${user.uid}`)
    }
    if (mediaType === 'audio'){
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}

let leaveTheChatsByUser = async () => {
    for(i=0;localsTracks.length >i; i++){
        localsTracks[i].stop()
        localsTracks[i].close()
    }
    await client.leave()
    window.open('/video_room_enter/','_self')
}
let cameraOnAndOff = async(event)=>{
    if(localsTracks[1].muted){
        await localsTracks[1].setMuted(false)
        event.target.style.background = '#fff'
    }
    else{
        await localsTracks[1].setMuted(true)
        event.target.style.background = 'rgba(255,80,81,1)'
    }
}
let MicrophoneOffandOn = async (event) =>{
    if(localsTracks[0].muted){
        await localsTracks[0].setMuted(false)
        event.target.style.background = '#fff'
    }
    else{
        await localsTracks[0].setMuted(true)
        event.target.style.background = 'rgba(255,80,81,1)'
    }
}
joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click',leaveTheChatsByUser)
document.getElementById('camera-btn').addEventListener('click',(e)=>{
    cameraOnAndOff(e)
})
document.getElementById('mic-btn').addEventListener('click',(e)=>{
    MicrophoneOffandOn(e)
})

let createMember = async () => {
    let res = await fetch('/createUser/',{
    method:'POST',
    headers:{
        'Content-Type':'application/json'
    },
    body:JSON.stringify({'name':NAME,'room_name':CHANNEL, 'UID':UID})
})
let member = await res.json()
return member
}
let getMembers = async (user) => {
    let res = fetch(`/getUsers/?UID=${user.uid}&room_name=${CHANNEL}`)
    let member = (await res).json()
    return member
}