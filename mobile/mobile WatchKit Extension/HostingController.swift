//
//  HostingController.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 3/24/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import WatchKit
import Foundation
import SwiftUI

class HostingController: WKHostingController<ContentView> {
    override var body: ContentView {
        return ContentView(motion: MotionManager())
    }
}
