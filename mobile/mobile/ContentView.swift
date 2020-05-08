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

//func sendLoginPost(patient_id: String, _ completion: @escaping (String?, String?, String?, String?, Int?) -> Void){
//    let parameters = ["patient_id": patient_id]
//    AF.request("http://http://sparkle-env-1.eba-b8vqgrb3.us-west-2.elasticbeanstalk.com/mobile-login",
//               method: .post,
//               parameters: parameters,
//               encoder: JSONParameterEncoder.default).responseDecodable(of: [rxMetadata].self) { response in
////                    debugPrint(response)
//                guard let schedule = response.value else { return }
//                let firstname = schedule[0].firstname
//                let timestamp = schedule[0].timestamp
//                let drug = schedule[0].drug
//                let desc = schedule[0].desc
//                let amount = schedule[0].amount
//                completion(firstname, timestamp, drug, desc, amount)
//    }
//}

// to catch the index out of range error
extension Collection {
    subscript(safe index: Index) -> Element? {
        return indices.contains(index) ? self[index] : nil
    }
}


class ContentViewModel: ObservableObject {
    // https://www.calincrist.com/blog/2020-04-12-how-to-get-notified-for-changes-in-swiftui/
    var patient_id: String = "" {
        willSet { // only updates view if patient_id > 1
            if patient_id.count > 1  {
                self.sendLoginPost()
                objectWillChange.send()
            }
        }
    }
    @Published var firstname: String = "" {
        didSet {
            loggedIn = (firstname.count > 1)
        }
    }
    @Published var nextTime: String = ""
    @Published var nextDrug: String = ""
    @Published var nextDesc: String = ""
    @Published var nextAmount: Int = 0
    @Published var loggedIn: Bool = false
    
    func sendLoginPost(){
        let parameters = ["patient_id": self.patient_id]
        AF.request("http://sparkle-env-1.eba-b8vqgrb3.us-west-2.elasticbeanstalk.com/mobile-login",
                   method: .post,
                   parameters: parameters,
                   encoder: JSONParameterEncoder.default).responseDecodable(of: [rxMetadata].self) { response in
                        debugPrint(response)
                    guard let schedule = response.value else { return }
                    self.firstname = schedule[safe: 0]!.firstname
                    self.nextTime = schedule[safe: 0]!.timestamp
                    self.nextDrug = schedule[safe: 0]!.drug
                    self.nextDesc = schedule[safe: 0]!.desc
                    self.nextAmount = schedule[safe: 0]!.amount
                    
//                    completion(self.firstname, self.nextTime, self.nextDrug, self.nextDesc, self.nextAmount)
        }
    }
}

// View
struct ContentView: View {
    @ObservedObject var viewModel = ContentViewModel()
    @State private var showNext: Bool = false
    var body: some View {
        VStack {
            Image("logo")
                .resizable()
                .scaledToFit()
            if self.viewModel.loggedIn == false {  // logged out
                TextField("Enter patient id here",
                          text: $viewModel.patient_id,
                          onCommit: { self.viewModel.sendLoginPost()
                })
                .textFieldStyle(RoundedBorderTextFieldStyle())
                Button(action: {
                    self.showNext = true
                }) {
                    Text("Fetch medication schedule")
                }
                .alert(isPresented: $showNext) {
                    Alert(title: Text("Welcome guy!"), message: Text("Wear sunscreen"), dismissButton: .default(Text("Got it!")))
                }
            } else {                               // logged in
                Toggle(isOn: $viewModel.loggedIn) {
                    Text("You're logged in")
                }
                
                Text("Welcome \(viewModel.firstname)!")
                Text("Don't forget to take \(viewModel.nextAmount) \(viewModel.nextDrug)'s at \(viewModel.nextTime) today!")
            }
            
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
