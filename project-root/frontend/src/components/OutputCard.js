/**
 * Output Card Component
 */
import React from 'react';
import { View, Text, ScrollView } from 'react-native';

const OutputCard = ({ accent, confidence, recommendations = [] }) => {
  return (
    <ScrollView style={{ padding: 16 }}>
      <View style={{
        backgroundColor: '#f5f5f5',
        padding: 16,
        borderRadius: 8,
        marginBottom: 16,
      }}>
        <Text style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 8 }}>
          Detected Accent
        </Text>
        <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#f50057' }}>
          {accent || 'Unknown'}
        </Text>
        <Text style={{ fontSize: 14, color: '#666', marginTop: 8 }}>
          Confidence: {(confidence * 100).toFixed(2)}%
        </Text>
      </View>

      {recommendations.length > 0 && (
        <View style={{
          backgroundColor: '#fff3e0',
          padding: 16,
          borderRadius: 8,
        }}>
          <Text style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 8 }}>
            Recommendations
          </Text>
          {recommendations.map((rec, index) => (
            <Text key={index} style={{ fontSize: 14, marginBottom: 4 }}>
              • {rec}
            </Text>
          ))}
        </View>
      )}
    </ScrollView>
  );
};

export default OutputCard;
