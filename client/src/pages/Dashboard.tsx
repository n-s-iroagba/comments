import React from "react"
import SocialMediaActionButton from "../components/SocialMediaActionButton"
import { faBars } from "@fortawesome/free-solid-svg-icons";

const Dashboard = ()=>{
    const replyCommentsActions = [
        {action: "Use", link: "/use/:reply-comments/:facebook",icon:faBars },
        { action: "Information", link: "/info/:reply-comments/:facebook",icon:faBars },
        { action: "How To Use", link: "/how-to-use/:reply-comments/:facebook",icon:faBars},

    ]
    const facebookBots = [
        {
            label: "Reply comments",
            icon :faBars
    }
    ]

    return<>
    <div>
    {
        facebookBots.map((bot,index)=>(
            <SocialMediaActionButton key={index} icon = {facebookBots[index].icon} label = {facebookBots[index].label} actions={replyCommentsActions} />
        ))
 
    }

    </div>
    
    
    </>
}
export default Dashboard

