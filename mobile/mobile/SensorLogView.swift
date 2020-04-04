//
//  SensorLogView.swift
//  mobile
//
//  Created by Collin Prather on 3/30/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI


struct SensorLogView: View {
    @ObservedObject
    var watchSession: WatchSessionManager
    
    var body: some View {
        ScrollView {
            Text("Lots to add")
            List(watchSession.messagesReceived) { message in
                Text(message.timestamp)
            }
        }
    }
}

struct SensorLogView_Previews: PreviewProvider {
    static var previews: some View {
        SensorLogView(watchSession: WatchSessionManager())
    }
}
