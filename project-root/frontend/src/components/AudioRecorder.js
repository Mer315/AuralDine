/**
 * Audio Recorder Component
 */
import React, { useState } from 'react';
import { View, TouchableOpacity, Text } from 'react-native';

const AudioRecorder = ({ onRecordingComplete }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingUri, setRecordingUri] = useState(null);

  const startRecording = async () => {
    // Placeholder implementation
    setIsRecording(true);
  };

  const stopRecording = async () => {
    // Placeholder implementation
    setIsRecording(false);
    if (onRecordingComplete) {
      onRecordingComplete(recordingUri);
    }
  };

  return (
    <View>
      <TouchableOpacity
        onPress={isRecording ? stopRecording : startRecording}
        style={{
          backgroundColor: isRecording ? 'red' : 'green',
          padding: 20,
          borderRadius: 50,
        }}
      >
        <Text style={{ color: 'white', textAlign: 'center' }}>
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

export default AudioRecorder;
