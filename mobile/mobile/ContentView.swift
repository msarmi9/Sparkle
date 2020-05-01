//
//  SensorView.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 3/20/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI
import Alamofire

let loginParameters: [String: String] = [
"patient_id": "2"
]

struct rxMetadata: Decodable {
    let firstname: String
    let timestamp: String
    let drug: String
    let desc: String
    let amount: Int
}

func sendLoginPost(patient_id: String, _ completion: @escaping (String?, String?, String?, String?, Int?) -> Void){
    let parameters = ["patient_id": patient_id]
    AF.request("http://twinkle3.us-west-2.elasticbeanstalk.com/mobile-login",
               method: .post,
               parameters: parameters,
               encoder: JSONParameterEncoder.default).responseDecodable(of: [rxMetadata].self) { response in
//                    debugPrint(response)
                guard let schedule = response.value else { return }
                let firstname = schedule[0].firstname
                let timestamp = schedule[0].timestamp
                let drug = schedule[0].drug
                let desc = schedule[0].desc
                let amount = schedule[0].amount
                completion(firstname, timestamp, drug, desc, amount)
    }
}


// View
struct ContentView: View {
    @State private var patient_id: String = ""
    @State private var firstname: String = ""
    @State private var loggedIn: Bool = false
    @State private var nextTime: String = ""
    @State private var nextDrug: String = ""
    @State private var nextDesc: String = ""
    @State private var nextAmount: Int = 0
    var body: some View {
        VStack {
            Title()
            TextField("Enter patient id here",
                      text: $patient_id,
                      onCommit: { sendLoginPost(patient_id: "1") { firstname, timestamp, drug, desc, amount in
                        guard case self.firstname = firstname else { return }
                        self.loggedIn = true
                        guard case self.nextTime = timestamp else { return }
                        guard case self.nextDrug = drug else { return }
                        guard case self.nextDesc = desc else { return }
                        guard case self.nextAmount = amount else { return }
                      } })
                .textFieldStyle(RoundedBorderTextFieldStyle())
            .alert(isPresented: $loggedIn) {
                Alert(title: Text("Welcome, \(self.firstname)"), message: Text("Don't forget to take \(nextAmount) \(nextDrug)'s at \(nextTime) today!"), dismissButton: .default(Text("Got it!")))
            }
            Text("Welcome \(firstname)!")
            Text("Don't forget to take \(nextAmount) \(nextDrug)'s at \(nextTime) today!")
            SeeSensors()
        }
    }
}

struct Title: View {
    var body: some View {
        HStack {
            Image(systemName: "star.fill")

            Text("Sparkle")
                .font(.system(size: 32)).italic()

            Image(systemName: "star.fill")
        }
    }
}

struct SeeSensors: View {
    var body: some View {
        NavigationView {
            HStack {
                Image(systemName: "antenna.radiowaves.left.and.right")
                    .font(.headline)
                // maybe want to use a button here..
                NavigationLink(destination: SensorLogView(watchSession: WatchSessionManager())){
                    Text("See recordings")
                }
            }
        }
    }
}

struct SensorView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
