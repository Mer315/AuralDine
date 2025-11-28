/**
 * Result Screen
 */
import React, { useState, useEffect } from 'react';
import { View, StyleSheet } from 'react-native';
import OutputCard from '../components/OutputCard';
import { accentService } from '../api/accentService';

const ResultScreen = ({ route, navigation }) => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        const recordingUri = route.params?.recordingUri;
        // Call API to get prediction
        const prediction = await accentService.predictAccent(recordingUri);
        setResult(prediction);
      } catch (error) {
        console.error('Error fetching prediction:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPrediction();
  }, [route.params]);

  if (loading) {
    return <View style={styles.container} />;
  }

  return (
    <View style={styles.container}>
      <OutputCard
        accent={result?.accent}
        confidence={result?.confidence}
        recommendations={result?.recommendations}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
});

export default ResultScreen;
