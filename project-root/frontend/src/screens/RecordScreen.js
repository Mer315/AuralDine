/**
 * Record Screen
 */
import React, { useState } from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';
import AudioRecorder from '../components/AudioRecorder';
import Loader from '../components/Loader';

const RecordScreen = ({ navigation }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [recordingUri, setRecordingUri] = useState(null);

  const handleRecordingComplete = (uri) => {
    setRecordingUri(uri);
    setIsLoading(true);
    
    // Simulate processing
    setTimeout(() => {
      setIsLoading(false);
      navigation.navigate('Result', { recordingUri: uri });
    }, 2000);
  };

  return (
    <View style={styles.container}>
      <AudioRecorder onRecordingComplete={handleRecordingComplete} />
      <Loader visible={isLoading} message="Processing audio..." />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
});

export default RecordScreen;
